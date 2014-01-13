# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Thomas Quintana <quintana.thomas@gmail.com>

from conf.settings import *
from lib.commands import *
from lib.esl import *
from lib.events import *
from lib.fsm import *
from lib.services import *
from pykka import ActorRegistry, ThreadingActor
from twisted.internet import reactor

import logging
import re
import sys

# Commands used only by the Freepy server.
class AuthCommand(object):
  def __init__(self, password):
    self.__password__ = password

  def __str__(self):
    return 'auth %s\n\n' % (self.__password__)

class EventsCommand(object):
  def __init__ (self, events, format = 'plain'):
    if(not format == 'json' and not format == 'plain' and not format == 'xml'):
      raise ValueError('The FreeSWITCH event socket only supports the \
        following formats: json, plain, xml')
    self.__events__ = events
    self.__format__ = format

  def __str__(self):
    return 'event %s %s\n\n' % (self.__format__, ' '.join(self.__events__))

# Events used only between the Dispatcher and the Dispatcher Proxy.
class InitializeDispatcherEvent(object):
  def __init__(self, apps, client):
    self.__apps__ = apps
    self.__client__ = client

  def get_apps(self):
    return self.__apps__

  def get_client(self):
    return self.__client__

class KillDispatcherEvent(object):
  pass

# The Core server components.
class ApplicationFactory(object):
  def __init__(self, dispatcher):
    self.__classes__ = dict()
    self.__singletons__ = dict()
    self.__init_event__ = InitializeSwitchletEvent(dispatcher)
    self.__uninit_event__ = UninitializeSwitchletEvent()

  def __contains_name__(self, name):
    if self.__classes__.has_key(name) or self.__singletons__.has_key(name):
      return True
    return False

  def __get_klass__(self, name):
    module = sys.modules.get(name)
    if not module:
      separator = name.rfind('.')
      path = name[:separator]
      klass = name[separator + 1:]
      module = __import__(path, globals(), locals(), [klass], -1)
      return getattr(module, klass)

  def get_instance(self, name):
    klass = self.__classes__.get(name)
    if klass:
      instance = klass().start()
      instance.tell({'content': self.__init_event__})
      return instance
    else:
      instance = self.__singletons__.get(name)
      return instance

  def register(self, name, type = 'class'):
    if self.__contains_name__(name):
      raise ValueError("Names must be unique across classes and singletons.\n\
      %s already exists please choose a different name and try again.",
      name)
    klass = self.__get_klass__(name)
    if type == 'class':
      self.__classes__.update({name: klass})
    if type == 'singleton':
      singleton = klass.start()
      singleton.tell({'content': self.__init_event__})
      self.__singletons__.update({name: singleton})

  def unregister(self, name):
    klass = self.__classes__.get(name)
    if klass:
      del self.__classes__[name]
    else:
      singleton = self.__singletons__.get(name)
      singleton.tell({'content': self.__uninit_event__})
      if singleton:
        singleton.stop()
        del self.__singletons__[name]

  def shutdown(self):
    # Cleanup the singletons being managed.
    names = self.__singletons__.keys()
    for name in names:
      self.unregister(name) 

class DispatcherProxy(IEventSocketClientObserver):
  def __init__(self, apps, dispatcher):
    self.__apps__ = apps
    self.__dispatcher__ = dispatcher

  def on_event(self, event):
    self.__dispatcher__.tell({'content': event})

  def on_start(self, client):
    event = InitializeDispatcherEvent(self.__apps__, client)
    self.__dispatcher__.tell({'content': event})

  def on_stop(self):
    event = KillDispatcherEvent()
    self.__dispatcher__.tell({'content': event})

class Dispatcher(FiniteStateMachine, ThreadingActor):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'authenticating'),
    ('authenticating', 'failed authentication'),
    ('authenticating', 'initializing'),
    ('initializing', 'failed initialization'),
    ('initializing', 'dispatching'),
    ('dispatching', 'dispatching'),
    ('dispatching', 'done')
  ]

  def __init__(self, *args, **kwargs):
    super(Dispatcher, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('freepy.lib.server.dispatcher')
    self.__observers__ = dict()
    self.__transactions__ = dict()

  @Action(state = 'authenticating')
  def __authenticate__(self, message):
    password = freeswitch_host.get('password')
    auth_command = AuthCommand(password)
    self.__client__.send(auth_command)

  @Action(state = 'done')
  def __cleanup__(self, message):
    self.__apps__.shutdown()
    self.stop()

  @Action(state = 'dispatching')
  def __dispatch__(self, message):
    if message:
      if isinstance(message, BackgroundCommand):
        self.__dispatch_command__(message)
      elif isinstance(message, RegisterJobObserverEvent):
        observer = message.get_observer()
        uuid = message.get_job_uuid()
        if observer and uuid:
          self.__observers__.update({uuid: observer})
      elif isinstance(message, UnregisterJobObserverEvent):
        uuid = message.get_job_uuid()
        if self.__observers__.has_key(uuid):
          del self.__observers__[uuid]
      else:
        headers = message.get_headers()
        content_type = headers.get('Content-Type')
        if content_type == 'command/reply':
          uuid = headers.get('Job-UUID')
          if uuid:
            self.__dispatch_response__(uuid, message)
        elif content_type == 'text/event-plain':
          uuid = headers.get('Job-UUID')
          if uuid:
            self.__dispatch_observer_event__(uuid, message)
          else:
            self.__dispatch_incoming__(message)

  def __dispatch_command__(self, message):
    # Make sure we can route the response to the right actor.
    uuid = message.get_job_uuid()
    sender = message.get_sender()
    self.__transactions__.update({uuid: sender})
    # Send the command.
    self.__client__.send(message)

  def __dispatch_incoming__(self, message):
    headers = message.get_headers()
    for rule in dispatch_rules:
      target = rule.get('target')
      name = rule.get('header_name')
      header = headers.get(name)
      if not header:
        continue
      value = rule.get('header_value')
      if value and header == value:
        self.__apps__.get_instance(target).tell({'content': message})
        return
      pattern = rule.get('header_pattern')
      if pattern:
        match = re.search(pattern, header)
        if match:
          self.__apps__.get_intance(target).tell({'content': message})
          return
    self.__logger__.info('No route was defined for the following message.\n \
    %s\n%s', str(message.get_headers()), str(message.get_body()))

  def __dispatch_observer_event__(self, uuid, message):
    recipient = self.__observers__.get(uuid)
    if recipient:
      recipient.tell({'content': message})

  def __dispatch_response__(self, uuid, message):
    recipient = self.__transactions__.get(uuid)
    if recipient:
      del self.__transactions__[uuid]
      recipient.tell({'content': message})

  @Action(state = 'initializing')
  def __initialize__(self, message):
    if 'BACKGROUND_JOB' not in dispatch_events:
      dispatch_events.append('BACKGROUND_JOB')
    events_command = EventsCommand(dispatch_events)
    self.__client__.send(events_command)

  def __on_auth__(self, message):
    if self.state() == 'not ready':
      self.transition(to = 'authenticating', event = message)

  def __on_command__(self, message):
    if self.state() == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def __on_command_reply__(self, message):
    reply = message.get_header('Reply-Text')
    if self.state() == 'authenticating':
      if reply == '+OK accepted':
        self.transition(to = 'initializing', event = message)
      elif reply == '-ERR invalid':
        self.transition(to = 'failed authentication', event = message)
    if self.state() == 'initializing':
      if reply == '+OK event listener enabled plain':
        self.transition(to = 'dispatching')
      elif reply == '-ERR no keywords supplied':
        self.transition(to = 'failed initialization', event = message)
    if self.state() == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def __on_event__(self, message):
    if self.state() == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def __on_init__(self, message):
    self.__apps__ = message.get_apps()
    self.__client__ = message.get_client()

  def __on_kill__(self, message):
    if self.state() == 'dispatching':
      self.transition(to = 'done', event = message)

  def __on_observer__(self, message):
    if self.state() == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def on_receive(self, message):
    # This is necessary because all Pykka messages
    # must be of type dict.
    message = message.get('content')
    if not message:
      return
    # Handle the message.
    if isinstance(message, Event):
      content_type = message.get_header('Content-Type')
      if content_type == 'auth/request':
        self.__on_auth__(message)
      elif content_type == 'command/reply':
        self.__on_command_reply__(message)
      elif content_type == 'text/event-plain':
        self.__on_event__(message)
    elif isinstance(message, BackgroundCommand):
      self.__on_command__(message)
    elif isinstance(message, RegisterJobObserverEvent):
      self.__on_observer__(message)
    elif isinstance(message, UnregisterJobObserverEvent):
      self.__on_observer__(message)
    elif isinstance(message, InitializeDispatcherEvent):
      self.__on_init__(message)
    elif isinstance(message, KillDispatcherEvent):
      self.__on_kill__(message)

class FreepyServer(object):
  def __init__(self, *args, **kwargs):
    self.__logger__ = logging.getLogger('freepy.lib.server.freepyserver')

  def __load_apps_factory__(self, dispatcher):
    factory = ApplicationFactory(dispatcher)
    for rule in dispatch_rules:
      target = rule.get('target')
      persistent = rule.get('persistent')
      if not persistent:
        factory.register(target, type = 'class')
      else:
        factory.register(target, type = 'singleton')
    return factory

  def __validate_rule__(self, rule):
    name = rule.get('header_name')
    value = rule.get('header_value')
    pattern = rule.get('header_pattern')
    target = rule.get('target')
    if not name or not target or not value and not pattern \
      or value and pattern:
      return False
    else:
      return True

  def start(self):
    # Initialize application wide logging.
    logging.basicConfig(filename = logging_filename, format = logging_format,
      level = logging_level)
    # Validate the list of rules.
    for rule in dispatch_rules:
      if not self.__validate_rule__(rule):
        self.__logger__.critical('The rule %s is invalid.', str(rule))
        return
    # Create a dispatcher thread.
    dispatcher = Dispatcher().start()
    # Load all the apps.
    apps = self.__load_apps_factory__(dispatcher)
    # Create the proxy between the event socket client and the dispatcher.
    dispatcher_proxy = DispatcherProxy(apps, dispatcher)
    # Create an event socket client factory and start the reactor.
    address = freeswitch_host.get('address')
    port = freeswitch_host.get('port')
    factory = EventSocketClientFactory(dispatcher_proxy)
    reactor.connectTCP(address, port, factory)
    reactor.run()

  def stop(self):
    ActorRegistry.stop_all()
  
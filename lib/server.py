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
from lib.fsm import *
from lib.services import *
from pykka import ActorRegistry, ThreadingActor
from twisted.internet import reactor

import logging
import re
import sys

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

class RegisterJobObserverEvent(object):
  def __init__(self, observer, uuid):
    self.__observer__ = observer
    self.__uuid__ = uuid

  def get_observer(self):
    return self.__observer__

  def get_uuid(self):
    return self.__uuid__

class UnregisterJobObserverEvent(object):
  def __init__(self, uuid):
    self.__uuid__ = uuid

  def get_uuid(self):
    return self.__uuid__

class DispatcherProxy(IEventSocketClientObserver):
  def __init__(self, apps, dispatcher):
    self.__apps__ = apps
    self.__dispatcher__ = dispatcher.start()

  def on_event(self, event):
    self.__dispatcher__.tell({'content': event})

  def on_start(self, client):
    event = InitializeDispatcherEvent(self.__apps__, client)
    self.__dispatcher__.tell({'content': event})

  def on_stop(self):
    event = KillDispatcherEvent()
    self.__dispatcher__.tell({'content': event})

class Dispatcher(FiniteStateMachine, ThreadingActor):
  state = 'not ready'

  transitions = [
    ('not ready', 'authenticating'),
    ('authenticating', 'failed authentication'),
    ('authenticating', 'initializing'),
    ('initializing', 'failed initialization'),
    ('initializing', 'dispatching'),
    ('dispatching', 'dispatching'),
    ('dispatching', 'done')
  ]

  def __init_(self, *args, **kwargs):
    super(Dispatcher, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('Dispatcher')
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
        uuid = message.get_uuid()
        self.__observers__.update({uuid: observer})
      elif isinstance(message, UnregisterJobObserverEvent):
        uuid = message.get_uuid()
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
    uuid = message.get_uuid()
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
      del self.__observers__[uuid]
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
    if self.state == 'not ready':
      self.transition(to = 'authenticating', event = message)

  def __on_command__(self, message):
    if self.state == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def __on_command_reply__(self, message):
    reply = message.get_header('Reply-Text')
    if self.state == 'authenticating':
      if reply == '+OK accepted':
        self.transition(to = 'initializing', event = message)
      elif reply == '-ERR invalid':
        self.transition(to = 'failed authentication', event = message)
    if self.state == 'initializing':
      if reply == '+OK event listener enabled plain':
        self.transition(to = 'dispatching')
      elif reply == '-ERR no keywords supplied':
        self.transition(to = 'failed initialization', event = message)

  def __on_event__(self, message):
    if self.state == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def __on_init__(self, message):
    self.__apps__ = message.get_apps()
    self.__client__ = message.get_client()

  def __on_kill__(self, message):
    if self.state == 'dispatching':
      self.transition(to = 'done', event = message)

  def __on_observer__(self, message):
    if self.state == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def on_receive(self, message):
    # This is necessary because all Pykka messages
    # must be of type dict.
    message = message.get('content')
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
    self.__logger__ = logging.getLogger('Freepy Server')

  def __load_apps_factory__(self):
    factory = ApplicationFactory()
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
    logging.basicConfig(format = logging_format, level = logging_level)
    # Validate the list of rules.
    for rule in dispatch_rules:
      if not self.__validate_rule__(rule):
        self.__logger__.critical('The rule %s is invalid.', str(rule))
        return
    # Load all the apps or log an error and return.
    apps = self.__load_apps_factory__()
    # Create a dispatcher thread.
    dispatcher = Dispatcher()
    dispatcher_proxy = DispatcherProxy(apps, dispatcher)
    # Create an event socket client factory and start the reactor.
    address = freeswitch_host.get('address')
    port = freeswitch_host.get('port')
    factory = EventSocketClientFactory(dispatcher_proxy)
    reactor.connectTCP(address, port, factory)
    reactor.run()

  def stop(self):
    ActorRegistry.stop_all()
  
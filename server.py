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

from actors import *
from commands import *
from esl import *
from fsm import *
from settings import *
from pykka import ActorRegistry, ThreadingActor

import logging
import re

class InitializeDispatcherEvent(object):
  def __init__(self, client):
    self.__client__ = client

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
  def __init__(self, dispatcher):
    self.__dispatcher__ = dispatcher

  def on_event(self, event):
    self.__dispatcher__.tell(event)

  def on_start(self, client):
    event = InitializeDispatcherEvent(client)
    self.__dispatcher__.tell(event)

  def on_stop(self):
    event = KillDispatcherEvent()
    self.__dispatcher__.tell(event)

class Dispatcher(ThreadingActor, FiniteStateMachine):
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

  def __init_(self):
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
    ActorRegistry.stop_all()

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

  def __dispatch_command__(self, command):
    # Make sure we can route the response to the right actor.
    uuid = command.get_uuid()
    sender = command.get_sender()
    self.__transactions__.update({uuid: sender})
    # Send the command.
    self.__client__.send(command)

  def __dispatch_incoming__(self, message):
    headers = message.get_headers()
    for rule in dispatch_rules:
      if not self.__validate_rule__(rule):
        self.__logger__.warning('The rule %s is invalid.', str(rule))
        continue
      name = rule.get('header_name')
      header = headers.get(name)
      if not header:
        continue
      value = rule.get('header_value')
      if value and header == value:
        rule.get('target').tell(message)
        return
      pattern = rule.get('header_pattern')
      if pattern:
        match = re.search(pattern, header)
        if match:
          rule.get('target').tell(message)
          return
    self.__logger__.info('No route was defined for the following message.\n \
    %s\n%s', str(message.get_headers()), str(message.get_body()))

  def __dispatch_observer_event__(self, uuid, message):
    recipient = self.__observers__.get(uuid)
    if recipient:
      del self.__observers__[uuid]
      recipient.tell(message)

  def __dispatch_response__(self, uuid, message):
    recipient = self.__transactions__.get(uuid)
    if recipient:
      del self.__transactions__[uuid]
      recipient.tell(message)

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

  @Action(state = 'initializing')
  def __initialize__(self, message):
    if 'BACKGROUND_JOB' not in dispatch_events:
      dispatch_events.append('BACKGROUND_JOB')
    events_command = EventsCommand(dispatch_events)
    self.__client__.send(events_command)

  def __on_auth__(self, message):
    if self.state == 'not ready':
      self.transition(to = 'authenticating', event = message)

  def __on_command__(self, command):
    if self.state == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def __on_command_reply__(self, message):
    reply = message['event'].get_header('Reply-Text')
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
    self.__client__ = message.get_client()

  def __on_kill__(self, message):
    if self.state == 'dispatching':
      self.transition(to = 'done', event = message)

  def __on_observer__(self, message):
    if self.state == 'dispatching':
      self.transition(to = 'dispatching', event = message)

  def on_receive(self, message):
    if isinstace(message, Event):
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

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
#
# Nishad Musthafa  <nishadmusthafa@gmail.com>

from lib.core import InitializeSwitchletEvent, Switchlet
from lib.fsm import Action, FiniteStateMachine
from lib.esl import Event
from switchlets.data_connector import DataConnector, QueryContext, QueryResult


import logging

class StartWaitingForCall(object):
  pass

class IncomingCallHandler(FiniteStateMachine, Switchlet):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'waiting for incoming call'),
    ('waiting for incoming call', 'call started. fetching app'),
    ('call started. fetching app', 'failed query. stopping call'),
    ('call started. fetching app', 'fetching execution logic'),
    ('fetching execution logic', 'failed query. stopping call'),
    ('fetching execution logic', 'got logic. executing logic'),
    ('failed query. stopping call', 'waiting for incoming call'),
    ('got logic. executing logic', 'waiting for incoming call'),
  ]

  def __init__(self, *args, **kwargs):
    super(IncomingCallHandler, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('heartbeat.monitor')
    self.__dispatcher__ = None
    self.__call_context__ = {}
    self.__data_connector__ = None

  def collect_call_context(self, message):
    call_context = {}
    # Right now, I'm putting in place a very trivial context of
    # 1. from number
    # 2. to number
    # 3. Call UUID
    # The idea is to use this information to figure out what to 
    # do with the call. Later iterations can have more complex 
    # To make this real general purpose, we can pass argument
    # 
    call_context['uuid'] = message.get_header('Channel-Call-UUID')
    call_context['from'] = message.get_header('Caller-Caller-ID-Number') # This can vary depending on the kind of call
    call_context['to'] = message.get_header('Caller-Destination-Number') # This can vary depending on the kind of call
    #TODO: Make the call contexts more general for multiple kinds of calls like
    # 1. SIP
    # 2. PSTN
    # 3. WebRTC
    self.__call_context__ = call_context

  @Action(state = 'call started. fetching app')
  def fetch_app(self, message):
    self.collect_call_context(message)
    self.__data_connector__ = DataConnector.start()
    query_data = {'caller_ref': self.actor_ref,
                  'model': 'number_mappings',
                  'key': self.__call_context__.get('to'),
                  'failure_destination_state': 'failed query. stopping call',
                  'success_destination_state': 'fetching execution logic'
                  }
    query_context = QueryContext(**query_data)
    self.__data_connector__.tell({'content': query_context})

  @Action(state = 'fetching execution logic')
  def find_call_execution_logic(self, message):
    query_data = {'caller_ref': self.actor_ref,
                  'model': 'app_data',
                  'key': message.get_query_result(),
                  'failure_destination_state': 'failed query. stopping call', 
                  'success_destination_state': 'got logic. executing logic'
                  }
    query_context = QueryContext(**query_data)
    self.__data_connector__.tell({'content': query_context})

  @Action(state = 'got logic. executing logic')
  def call_execution(self, message):
    self.__logger__.info('Logic to be executed is %s' % message.get_query_result())
    self.__data_connector__.stop()
    pass

  @Action(state = 'failed query. stopping call')
  def call_rejection(self, message):
    self.__data_connector__.stop()
    self.transition(to = 'waiting for incoming call')

  def on_receive(self, message):
    message = message.get('content')
    if isinstance(message, InitializeSwitchletEvent):
      self.transition(to = 'waiting for incoming call', event = message)
    elif isinstance(message, QueryResult):
      self.transition(to = message.get_destination_state(), event = message)
    elif isinstance(message, Event):
      content_type = message.get_header('Content-Type')

      if content_type == 'text/event-plain':
        name = message.get_header('Event-Name')
        call_direction = message.get_header('Caller-Direction')
        if name == 'CHANNEL_CREATE' and call_direction == 'inbound':
          self.transition(to = 'call started. fetching app', event = message)


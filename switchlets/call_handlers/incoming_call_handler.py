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

from lib.commands import AnswerCommand, KillCommand
from lib.core import InitializeSwitchletEvent, Switchlet
from lib.esl import Event
from lib.fsm import Action, FiniteStateMachine
from lib.server import RegisterJobObserverCommand, UnregisterJobObserverCommand
from switchlets.data_connector import DataConnector, QueryContext, QueryResult
from switchlets.call_utilities import ActionExecutor, StartExecution, ExecutionComplete


import logging

class StartWaitingForCall(object):
  pass

class EndCall(object):
  pass

class IncomingCallHandler(FiniteStateMachine, Switchlet):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'waiting for incoming call'),
    ('waiting for incoming call', 'call started. fetching app'),
    ('call started. fetching app', 'failed query. stopping call'),
    ('call started. fetching app', 'fetching execution logic'),
    ('fetching execution logic', 'failed query. stopping call'),
    ('fetching execution logic', 'got logic. answering call'),
    ('got logic. answering call', 'executing call logic'),
    ('failed query. stopping call', 'terminate call'),
    ('executing call logic', 'terminate call'),
    ('terminate call', 'call terminated'),
  ]

  def __init__(self, *args, **kwargs):
    super(IncomingCallHandler, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('switchlets.call_handlers.incoming_call_handler')
    self.__dispatcher__ = None
    self.__call_context__ = {}
    self.__data_connector__ = None
    self.__action_executor__ = None
    self.__execution_actions__ = None

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
    #TODO: Make the call contexts more general considering multiple kinds of calls like
    # 1. SIP
    # 2. PSTN
    # 3. WebRTC
    self.__call_context__ = call_context

  def get_call_uuid(self):
    return self.__call_context__.get('uuid')

  def initialize(self, message):
    self.__dispatcher__ = message.get_dispatcher()

  @Action(state = 'call started. fetching app')
  def fetch_app(self, message):
    self.collect_call_context(message)
    self.__data_connector__ = DataConnector.start()
    query_data = {'sender': self.actor_ref,
                  'model': 'number_mappings',
                  'key': self.__call_context__.get('to'),
                  'failure_destination_state': 'failed query. stopping call',
                  'success_destination_state': 'fetching execution logic'
                  }
    query_context = QueryContext(**query_data)
    self.__data_connector__.tell({'content': query_context})

  @Action(state = 'fetching execution logic')
  def find_call_execution_logic(self, message):
    query_data = {'sender': self.actor_ref,
                  'model': 'app_data',
                  'key': message.get_query_result(),
                  'failure_destination_state': 'failed query. stopping call', 
                  'success_destination_state': 'got logic. answering call'
                  }
    query_context = QueryContext(**query_data)
    self.__data_connector__.tell({'content': query_context})

  @Action(state = 'got logic. answering call')
  def call_answer(self, message):
    self.__execution_actions__ = message.get_query_result()
    self.__data_connector__.stop()
    answer_command = AnswerCommand(self.actor_ref, self.get_call_uuid())
    register_observer = RegisterJobObserverCommand(self.actor_ref, answer_command.get_job_uuid())
    self.__dispatcher__.tell({'content': register_observer})
    self.__dispatcher__.tell({'content': answer_command})


  @Action(state = 'executing call logic')
  def call_execution(self, message):
    execution_actions = self.__execution_actions__
    self.__logger__.info('Logic to be executed is for %s is %s' % 
                        (self.get_call_uuid(),
                         execution_actions))
    self.__action_executor__ = ActionExecutor.start()
    execution_params = {
                        'context': execution_actions,
                        'dispatcher': self.__dispatcher__,
                        'sender': self.actor_ref,
                        'call_uuid': self.get_call_uuid()
                        }
    start_execution = StartExecution(**execution_params)
    self.__action_executor__.tell({'content': start_execution})

  @Action(state = 'failed query. stopping call')
  def call_rejection(self, message):
    self.__data_connector__.stop()
    self.actor_ref.tell({'content': EndCall()})

  @Action(state = 'terminate call')
  def clean_up_call(self, message):
    kill_command = KillCommand(self.actor_ref, self.get_call_uuid())
    register_observer = RegisterJobObserverCommand(self.actor_ref, kill_command.get_job_uuid())
    self.__dispatcher__.tell({'content': register_observer})
    self.__dispatcher__.tell({'content': kill_command})


  @Action(state = 'call terminated')
  def end_call(self, message):
    if self.__action_executor__:
      self.__action_executor__.stop()
    # self.actor_ref.stop()

  def on_receive(self, message):
    message = message.get('content')

    if isinstance(message, InitializeSwitchletEvent):
      self.initialize(message)
      self.transition(to = 'waiting for incoming call')
    elif isinstance(message, EndCall) or isinstance(message, ExecutionComplete):
      self.transition(to = 'terminate call')
    elif isinstance(message, QueryResult):
      self.transition(to = message.get_destination_state(), event = message)
    elif isinstance(message, Event):
      content_type = message.get_header('Content-Type')

      if content_type == 'text/event-plain':
        name = message.get_header('Event-Name')
        call_direction = message.get_header('Caller-Direction')
        
        if name == 'CHANNEL_CREATE' and call_direction == 'inbound':
          self.transition(to = 'call started. fetching app', event = message)

        job_command_arg = message.get_header('Job-Command-Arg')
        job_command = message.get_header('Job-Command')
        
        if name == 'BACKGROUND_JOB' and job_command_arg == self.get_call_uuid() and job_command == 'uuid_answer':
          unregister_observer = UnregisterJobObserverCommand(job_command_arg)
          self.__dispatcher__.tell({'content': unregister_observer})
          self.transition(to = 'executing call logic', event = message)
        if name == 'BACKGROUND_JOB' and job_command_arg == self.get_call_uuid() and job_command == 'uuid_kill':
          unregister_observer = UnregisterJobObserverCommand(job_command_arg)
          self.__dispatcher__.tell({'content': unregister_observer})
          self.transition(to = 'call terminated', event = message)

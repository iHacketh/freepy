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
# Nishad Musthafa <nishadmusthafa@gmail.com>

from lib.core import InitializeSwitchletEvent, Switchlet
from lib.fsm import Action, FiniteStateMachine
from switchlets.ivr.menu import IVRMenu
from play import Play
import logging
from utils import StartExecution, ExecutionComplete

class ActionExecutor(FiniteStateMachine, Switchlet):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'waiting'),
    ('waiting', 'executing'),
    ('waiting', 'complete'),
    ('executing', 'executing'),
    ('executing', 'complete'),
  ]
  action_map = {
                'IVR' : IVRMenu,
                'Play': Play,
                }

  def __init__(self, *args, **kwargs):
    super(ActionExecutor, self).__init__(*args, **kwargs)
    self.__dispatcher__ = None
    self.__actions__ = None
    self.__sender__ = None
    self.__action_actor__ = None
    self._call_uuid = None
    self.__logger__ = logging.getLogger('switchlets.call_handlers.action_executor.ActionExecutor')
    self.transition(to = 'waiting')

  def configure(self, message):
    self.__dispatcher__ = message.get_dispatcher()
    self.__actions__ = message.get_context()
    self.__sender__ = message.get_sender()
    self.__call_uuid__ = message.get_call_uuid()

  def get_next_action(self):
    try:
      action = self.__actions__[0]
    except IndexError:
      action = None

    self.__actions__ = self.__actions__[1:]
    return action

  def execute_actions(self, message):
    action = self.get_next_action()
    if not action:
      self.transition(to = 'complete')
    else:
      self.transition(to = 'executing', event = action)

  def get_call_uuid(self):
    return self.__call_uuid__

  @Action(state = 'complete')
  def complete_executions(self, event):
    execution_complete = ExecutionComplete()
    self.__sender__.tell({'content': execution_complete})

  @Action(state = 'executing')
  def executing_call(self, action):
    self.__action_actor__ = self.action_map.get(action[0]).start()
    try:
      action_params = action[1]
    except IndexError:
      action_params = None
    execution_params = {
                        'context': action_params,
                        'dispatcher': self.__dispatcher__,
                        'sender': self.actor_ref,
                        'call_uuid': self.get_call_uuid()
                        }
    start_execution = StartExecution(**execution_params)
    self.__action_actor__.tell({'content': start_execution})

  def on_receive(self, message):
    message = message.get('content')
    if isinstance(message, StartExecution):
      self.configure(message)
      self.execute_actions(message)
    elif isinstance(message, ExecutionComplete):
      self.__action_actor__.stop()
      self.execute_actions(message)


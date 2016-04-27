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

# from lib.esl import Event
# from lib.server import Dispatcher, WatchEventCommand, UnwatchEventCommand
# from switchlets.call_utilities.play import PlayCommand, Play
# from switchlets.call_utilities.utils import StartExecution
import mock, time
from switchlets.call_utilities import ActionExecutor, ExecutionComplete, StartExecution
from unittest import TestCase



class ActionExecutorTests(TestCase):
  def test_flow(self):
    action_executor = ActionExecutor.start()
    with mock.patch('switchlets.call_utilities.play.Play.on_receive') as mock_play_on_receive:
      mock_sender = mock.Mock()
      execution_params = {
                          'context': [('Play', 'play_url_1'), ('Play', 'play_url_2'), ('Play', 'play_url_3')],
                          'dispatcher': 'mock_dispatcher',
                          'sender': mock_sender,
                          'call_uuid': 'fake_call_uuid'
                          }
      # State 'waiting' to 'executing'
      start_execution = StartExecution(**execution_params)
      action_executor.tell({'content': start_execution})
      time.sleep(2)

      action_receiver_call_count = mock_play_on_receive.call_count
      action_message = mock_play_on_receive.call_args_list[0][0][0]['content']

      self.assertTrue(action_receiver_call_count, 1)
      self.assertTrue(isinstance(action_message, StartExecution))
      self.assertEquals(action_message.get_context(), 'play_url_1')
      self.assertEquals(action_message.get_call_uuid(), 'fake_call_uuid')
      self.assertEquals(action_message.get_dispatcher(), 'mock_dispatcher')
      self.assertEquals(action_message.get_sender().actor_urn, action_executor.actor_urn)

      # State 'executing' to 'executing'
      completed_execution = ExecutionComplete()
      action_executor.tell({'content': completed_execution})
      time.sleep(2)

      action_receiver_call_count = mock_play_on_receive.call_count
      action_message = mock_play_on_receive.call_args_list[1][0][0]['content']
      
      self.assertTrue(action_receiver_call_count, 2)
      self.assertTrue(isinstance(action_message, StartExecution))
      self.assertEquals(action_message.get_context(), 'play_url_2')
      self.assertEquals(action_message.get_call_uuid(), 'fake_call_uuid')
      self.assertEquals(action_message.get_dispatcher(), 'mock_dispatcher')
      self.assertEquals(action_message.get_sender().actor_urn, action_executor.actor_urn)

      # State 'executing' to 'executing'
      completed_execution = ExecutionComplete()
      action_executor.tell({'content': completed_execution})
      time.sleep(2)

      action_receiver_call_count = mock_play_on_receive.call_count
      action_message = mock_play_on_receive.call_args_list[2][0][0]['content']
      
      self.assertTrue(action_receiver_call_count, 3)
      self.assertTrue(isinstance(action_message, StartExecution))
      self.assertEquals(action_message.get_context(), 'play_url_3')
      self.assertEquals(action_message.get_call_uuid(), 'fake_call_uuid')
      self.assertEquals(action_message.get_dispatcher(), 'mock_dispatcher')
      self.assertEquals(action_message.get_sender().actor_urn, action_executor.actor_urn)

      # State 'executing' to 'complete'
      completed_execution = ExecutionComplete()
      action_executor.tell({'content': completed_execution})
      time.sleep(2)

      self.assertEquals(mock_sender.mock_calls[0].call_list()[0][0], 'tell')
      sender_message = mock_sender.mock_calls[0].call_list()[0][1][0]['content']
      self.assertTrue(isinstance(sender_message, ExecutionComplete))

      action_executor.stop()

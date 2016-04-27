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

from lib.esl import Event
from lib.server import Dispatcher, WatchEventCommand, UnwatchEventCommand
from switchlets.call_utilities.play import PlayCommand, Play
from switchlets.call_utilities.utils import StartExecution
import mock, time
from unittest import TestCase


class PlayCommandTests(TestCase):
  def test_success_scenario(self):
    command = PlayCommand(object(), 'sample_call_uuid', path='some/music/file.wav')
    desired_output = 'sendmsg sample_call_uuid\ncall-command: execute\nexecute-app-name: playback\ncontent-type: text/plain\ncontent-length: 19\n\nsome/music/file.wav\n'
    self.assertTrue(str(command) == desired_output)


class PlayTests(TestCase):
  def test_play_flow_success(self):
    play = Play.start()
    with mock.patch('lib.server.Dispatcher.on_receive') as mock_on_receive:
      dispatcher = Dispatcher().start()

      execution_params = {
                          'context': 'play_url',
                          'dispatcher': dispatcher,
                          'sender': object(),
                          'call_uuid': 'fake_call_uuid'
                          }
      start_execution = StartExecution(**execution_params)

      # State 'ready' to 'sending play command'
      play.tell({'content': start_execution})
      time.sleep(2)
      on_play_call_count = mock_on_receive.call_count
      on_play_passed_message_first = mock_on_receive.call_args_list[0][0][0]
      on_play_passed_message_second = mock_on_receive.call_args_list[1][0][0]
      on_play_passed_message_third = mock_on_receive.call_args_list[2][0][0]
      playback_stop_headers = {
                              'Content-Type':'text/event-plain',
                              'Event-Name': 'PLAYBACK_STOP',
                              'Channel-Call-UUID': 'fake_call_uuid'}
      playback_stop = Event(playback_stop_headers)

      # State 'sending play command' to 'complete'
      play.tell({'content': playback_stop})
      time.sleep(2)
      on_playback_stop_call_count = mock_on_receive.call_count
      on_playback_stop_message_first = mock_on_receive.call_args_list[3][0][0]
      on_playback_stop_message_second = mock_on_receive.call_args_list[4][0][0]

    self.assertTrue(on_play_call_count, 3)
    self.assertTrue(isinstance(on_play_passed_message_first['content'], WatchEventCommand))
    self.assertTrue(isinstance(on_play_passed_message_second['content'], WatchEventCommand))
    self.assertTrue(isinstance(on_play_passed_message_third['content'], PlayCommand))
    passed_play_command = on_play_passed_message_third['content']
    self.assertEquals('playback', passed_play_command.__app_name__)
    self.assertEquals('fake_call_uuid', passed_play_command.__uuid__)
    desired_play_command_output = 'sendmsg fake_call_uuid\ncall-command: execute\nexecute-app-name: playback\ncontent-type: text/plain\ncontent-length: 8\n\nplay_url\n'
    self.assertEquals(desired_play_command_output, str(passed_play_command))
    self.assertTrue(on_playback_stop_call_count, 5)
    self.assertTrue(isinstance(on_playback_stop_message_first['content'], UnwatchEventCommand))
    self.assertTrue(isinstance(on_playback_stop_message_second['content'], UnwatchEventCommand))

    dispatcher.stop()
    play.stop()

  def test_play_flow_error(self):
    play = Play.start()
    with mock.patch('lib.server.Dispatcher.on_receive') as mock_on_receive:
      dispatcher = Dispatcher().start()

      execution_params = {
                          'context': 'play_url',
                          'dispatcher': dispatcher,
                          'sender': object(),
                          'call_uuid': 'fake_call_uuid'
                          }
      start_execution = StartExecution(**execution_params)

      # State 'ready' to 'sending play command'
      play.tell({'content': start_execution})
      time.sleep(2)
      on_play_call_count = mock_on_receive.call_count
      on_play_passed_message_first = mock_on_receive.call_args_list[0][0][0]
      on_play_passed_message_second = mock_on_receive.call_args_list[1][0][0]
      on_play_passed_message_third = mock_on_receive.call_args_list[2][0][0]
      channel_execute_headers = {
                              'Content-Type':'text/event-plain',
                              'Event-Name': 'CHANNEL_EXECUTE_COMPLETE',
                              'Channel-Call-UUID': 'fake_call_uuid',
                              'Application': 'playback',
                              'Application-Data':'play_url',
                              'Application-Response': 'FILE NOT FOUND'}
      channel_executed = Event(channel_execute_headers)

      # State 'sending play command' to 'complete'
      play.tell({'content': channel_executed})
      time.sleep(2)
      on_channel_executed_call_count = mock_on_receive.call_count
      on_channel_executed_message_first = mock_on_receive.call_args_list[3][0][0]
      on_channel_executed_message_second = mock_on_receive.call_args_list[3][0][0]

    self.assertTrue(on_play_call_count, 3)
    self.assertTrue(isinstance(on_play_passed_message_first['content'], WatchEventCommand))
    self.assertTrue(isinstance(on_play_passed_message_second['content'], WatchEventCommand))
    self.assertTrue(isinstance(on_play_passed_message_third['content'], PlayCommand))
    passed_play_command = on_play_passed_message_third['content']
    self.assertEquals('playback', passed_play_command.__app_name__)
    self.assertEquals('fake_call_uuid', passed_play_command.__uuid__)
    desired_play_command_output = 'sendmsg fake_call_uuid\ncall-command: execute\nexecute-app-name: playback\ncontent-type: text/plain\ncontent-length: 8\n\nplay_url\n'
    self.assertEquals(desired_play_command_output, str(passed_play_command))
    self.assertEquals(on_channel_executed_call_count, 5)
    self.assertTrue(isinstance(on_channel_executed_message_first['content'], UnwatchEventCommand))
    self.assertTrue(isinstance(on_channel_executed_message_second['content'], UnwatchEventCommand))

    dispatcher.stop()
    play.stop()
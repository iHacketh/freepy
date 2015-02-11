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

from lib.server import Dispatcher
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
  def test_play_flow(self):
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
      play.tell({'content': start_execution})
      time.sleep(5.0)
      command = PlayCommand(object(), 'fake_call_uuid', path='play_url')
      passed_message = mock_on_receive.call_args[0][0]

    self.assertTrue(isinstance(passed_message['content'], PlayCommand))
    passed_command = passed_message['content']
    self.assertEquals('playback', passed_command.__app_name__)
    dispatcher.stop()
    play.stop()


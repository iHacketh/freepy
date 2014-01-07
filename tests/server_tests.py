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

from lib.server import *
from unittest import TestCase, expectedFailure

class AuthCommandTests(TestCase):
  def test_success_scenario(self):
    command = AuthCommand('ClueCon')
    self.assertTrue(str(command) == 'auth ClueCon\n\n')

class EventsCommandTests(TestCase):
  def test_success_scenario_with_multiple_events(self):
    command = EventsCommand(['BACKGROUND_JOB', 'HEARTBEAT'])
    self.assertTrue(str(command) == 'event plain BACKGROUND_JOB HEARTBEAT\n\n')

  def test_success_scenario_with_single_event(self):
    command = EventsCommand(['BACKGROUND_JOB'])
    self.assertTrue(str(command) == 'event plain BACKGROUND_JOB\n\n')

  def test_invalid_format(self):
    self.assertRaises(ValueError, EventsCommand, ['BACKGROUD_JOB'], format = 'invalid')

#class DispatcherTests(TestCase):
#  def test_startup_process(self):
#    pass

#  def test_background_jobs(self):
#    pass

#  def test_send_command(self):
#    pass
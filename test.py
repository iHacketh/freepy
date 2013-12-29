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

from commands import *
from esl import *
from twisted.internet import reactor
from unittest import TestCase, expectedFailure

import logging

# Initialize application wide logging.
logging.basicConfig(level = logging.DEBUG)

class EventSocketClientTests(TestCase):
  def test_successful_authentication(self):
    # Start the test.
    factory = EventSocketClientFactory(observer)
    reactor.connectTCP('192.168.1.106', 8021, factory)
    reactor.run()
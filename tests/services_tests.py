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

from lib.core import *
from lib.services import *
from pykka import ActorRegistry
from unittest import TestCase

import logging, time

logging.basicConfig(
  format = '%(asctime)s %(levelname)s - %(name)s - %(message)s',
  level = logging.DEBUG
)

class WaitingSwitchlet(Switchlet):
  def __init__(self, *args, **kwargs):
    super(WaitingSwitchlet, self).__init__(*args, **kwargs)
    self.__seconds__ = 0

  def on_receive(self, message):
    message = message.get('content')
    if isinstance(message, TimeoutEvent):
      self.__seconds__ += 1
      print self.__seconds__

class TimerServiceTests(TestCase):
  @classmethod
  def tearDownClass(cls):
    ActorRegistry.stop_all()

  def test_one_timer(self):
    service = TimerService().start()
    consumer = WaitingSwitchlet().start()
    command = ReceiveTimeoutCommand(consumer, 1000, recurring = True)
    service.tell({'content': command})
    time.sleep(150.0)
    service.stop()
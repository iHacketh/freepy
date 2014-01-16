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

import logging, math, time

logging.basicConfig(
  format = '%(asctime)s %(levelname)s - %(name)s - %(message)s',
  level = logging.DEBUG
)

class TickSwitchlet(Switchlet):
  def __init__(self, *args, **kwargs):
    super(TickSwitchlet, self).__init__(*args, **kwargs)
    self.__tick__ = 0

  def on_receive(self, message):
    message = message.get('content')
    if isinstance(message, TimeoutEvent):
      self.__tick__ += 1
      print self.__tick__

class SecondsSwitchlet(Switchlet):
  def __init__(self, *args, **kwargs):
    super(SecondsSwitchlet, self).__init__(*args, **kwargs)
    self.__last_time__ = 0
    self.__misses__ = 0

  def on_receive(self, message):
    message = message.get('content')
    if isinstance(message, TimeoutEvent):
      now = time.time()
      if self.__last_time__ > 0:
        skew = 1000 - math.trunc((now - self.__last_time__) * 1000)
        if skew > 100:
          self.__misses__ += 1
        print 'last time: %f, now: %f, skew: %ims' % (self.__last_time__, now, skew)
      self.__last_time__ = now

class TimerServiceTests(TestCase):
  @classmethod
  def tearDownClass(cls):
    ActorRegistry.stop_all()

  def test_recurring_timer_one_second_interval(self):
    # Start the timer service.
    service = TimerService().start()
    # Start the seconds switchlet.
    consumer = SecondsSwitchlet().start()
    # Tell the timer service to send timeout events to the seconds switchlet every second.
    command = ReceiveTimeoutCommand(consumer, 1000, recurring = True)
    service.tell({'content': command})
    # Wait for 1 minute worth of events to fire.
    time.sleep(60.0)
    # Make the timer service did not miss any deadlines.
    print 'misses: %i' % consumer._actor.__misses__
    self.assertTrue( consumer._actor.__misses__ == 0)
    # cleanup.
    service.stop()
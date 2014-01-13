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

from ctypes import *
from llist import dllist
from pykka import ThreadingActor

import logging, os

class ReceiveTimeoutCommand(object):
  def __init__(self, sender, timeout, recurring = False):
    self.__sender__ = sender
    self.__timeout__ = timeout
    self.__recurring__ = recurring

  def get_sender(self):
    return self.__sender__

  def get_timeout(self):
    return self.__timeout__

  def is_recurring(self):
    return self.__recurring__

class StopTimeoutCommand(object):
  def __init__(self, sender):
    self.__sender__ = sender

  def get_sender(self):
    return self.__sender__

class TimeoutEvent(object):
  pass

class TimerService(ThreadingActor):
  '''
  The timer service uses a timing wheel with a single thread borrowing
  from the approach used in the Linux kernel. Please refer to the email
  thread by Ingo Molnar @ https://lkml.org/lkml/2005/10/19/46.
  '''
  CLOCK_MONOTONIC = 1         # Use a monotonic clock.
  TICK_SIZE = 0.01            # Tick every 100 milliseconds.

  def __init__(self):
    # Initialize the timing wheels. The finest possible
    # granularity is 100ms.
    self.__timer_vector1__ = [dllist()] * 256
    self.__timer_vector2__ = [dllist()] * 256
    self.__timer_vector3__ = [dllist()] * 256
    # Initialize the timer vector indices.
    self.__timer_vector2_index__  = 0
    self.__timer_vector3_index__  = 0
    # Initialize the tick counter.
    self.__current_tick__ = 0
    # Initialize the actor lookup table for O(1) timer removal.
    self.__actor_lookup_table__ = dict()
    # Singleton instance of the timeout event.
    self.__timeout__ = TimeoutEvent()

  def __create_timer__(self):
    pass

  def __destroy_timer__(self, message):
    pass

  def __schedule__(self, timer):
    timeout = timer.get_timeout()
    if timeout <= 25600:
      self.__vector1_insert__(timer)
    elif timeout <= 6553600:
      self.__vector2_insert__(timer)
    elif timeout <= 1677721600:
      self.__vector3_insert__(timer)

  def __cascade_vector_2__(self):
    index = self.__timer_vector2_index__
    timers = self.__timer_vector2__.get(index)
    for timer in timers:
      self.__vector1_insert__(timer)
    timers.clear()
    index = (index + 1) % 256
    if index == 0:
      self.__cascade_vector_3__()

  def __cascade_vector_3__(self):
    index = self.__timer_vector3_index__
    timers = self.__timer_vector3__.get(index)
    for timer in timers:
      self.__vector2_insert__(timer)
    timers.clear()
    index = (index + 1) % 256

  def __tick__(self):
    tick = self.__current_tick__
    timers = self.__jiffies_wheel__.get(tick % 256)
    for timer in timers:
      timer.get_sender().tell({'content': self.__timeout__})
    self.__current_tick__ = tick + 1
    if self.__current_tick__ % 256 == 0:
      self.__cascade_vector_2__()

  def __unschedule__(self, timer):
    urn = timer.get_sender().actor_urn
    node = self.__actor_lookup_table__.get(urn)
    if node:
      del self.__actor_lookup_table__[urn]
      node.prev.next = node.next
      node.next.prev = node.prev

  def __update_actor_lookup_table__(self, node):
    urn = node.value.get_sender().actor_urn
    self.__actor_lookup_table__.update({urn: node})

  def __vector1_insert__(self, timer):
    bucket = timer.get_timeout() / 100
    node = self.__timer_vector1__.get(bucket).append(timer)
    self.__update_actor_lookup_table__(node)

  def __vector2_insert__(self, timer):
    bucket = timer.get_timeout() / 25600
    node = self.__timer_vector2__.get(bucket).append(timer)
    self.__update_actor_lookup_table__(node)

  def __vector3_insert__(self, timer):
    bucket = timer.get_timeout() / 6553600
    node = self.__timer_vector3__.get(bucket).append(timer)
    self.__update_actor_lookup_table__(node)

  def on_receive(self, message):
    # This is necessary because all Pykka messages
    # must be of type dict.
    message = message.get('content')
    if not message:
      return
    # Handle the message.
    if isinstance(message, ReceiveTimeoutCommand):
      self.__schedule__(message)
    elif isinstance(message, StopTimeoutCommand):
      self.__unschedule__(message)

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

from pykka import ThreadingActor

import logging
import sys
import types

class ApplicationFactory(object):
  def __init__(self):
    self.__classes__ = dict()
    self.__singletons__ = dict()

  def __contains_name__(self, name):
    if self.__classes__.has_key(name) or self.__singletons__.has_key(name):
      return True
    return False

  def __get_klass__(self, name):
    module = sys.modules.get(name)
    if not module:
      separator = name.rfind('.')
      path = name[:separator]
      klass = name[separator + 1:]
      module = __import__(path, globals(), locals(), [klass], -1)
      return getattr(module, klass)

  def get_instance(self, name):
    klass = self.__classes__.get(name)
    if klass:
      instance = klass().start()
      return instance
    else:
      instance = self.__singletons__.get(name)
      return instance

  def register(self, name, type = 'class'):
    if self.__contains_name__(name):
      raise ValueError("Names must be unique across classes and singletons.\n\
      %s already exists please choose a different name and try again.",
      name)
    klass = self.__get_klass__(name)
    if type == 'class':
      self.__classes__.update({name: klass})
    if type == 'singleton':
      singleton = klass.start()
      self.__singletons__.update({name: singleton})

  def unregister(self, name):
    klass = self.__classes__.get(name)
    if klass:
      del self.__classes__[name]
    else:
      singleton = self.__singletons__.get(name)
      if singleton:
        singleton.stop()
        del self.__singletons__[name]

  def shutdown(self):
    # Cleanup the singletons being managed.
    names = self.__singletons__.keys()
    for name in names:
      self.unregister(name) 

class TimerService(object):
  pass

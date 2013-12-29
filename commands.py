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

from uuid import uuid4

class AuthCommand(object):
  def __init__(self, password):
    self.__password__ = password

  def __str__(self):
    return 'auth %s\n\n' % (self.__password__)

class EventsCommand(object):
  def __init__ (self, events, format = 'plain'):
    if(not format == 'json' and not format == 'plain' and not format == 'xml'):
      raise ValueError('The FreeSWITCH event socket only supports the \
        following formats: json, plain, xml')
    self.__events__ = events
    self.__format__ = format

  def __str__(self):
    return 'event %s %s\n\n' % (self.__format__, ' '.join(self.__events__))

class BackgroundCommand(object):
  def __init__(self, sender):
    self.__sender__ = sender
    self.__uuid__ = uuid4().bytes

  def get_uuid(self):
    return self.__uuid__

  def get_sender(self):
    return self.__sender__

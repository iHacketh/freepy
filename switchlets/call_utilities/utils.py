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
# Nishad Musthafa <nishadmusthafa@gmail.com>

from lib.commands import UUIDCommand

class StartExecution(object):
  def __init__(self, **kwargs):
    try:
      self.__context__ = kwargs['context']
      self.__dispatcher__ = kwargs['dispatcher']
      self.__sender__ = kwargs['sender']
      self.__call_uuid__ = kwargs['call_uuid']
    except KeyError, e:
      self.__logger__.error('StartExecution initialized without mandatory parameter %s' % e)
      raise e

  def get_context(self):
    return self.__context__

  def get_dispatcher(self):
    return self.__dispatcher__

  def get_call_uuid(self):
    return self.__call_uuid__

  def get_sender(self):
    return self.__sender__

class ExecutionComplete(object):
  pass


class SendMessageCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(SendMessageCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'sendmsg %s\ncall-command: execute\nexecute-app-name: %s\n' % (self.__uuid__,
            self.__app_name__)
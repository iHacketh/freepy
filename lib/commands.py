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

# Import the proper StringIO implementation.
try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

class BackgroundCommand(object):
  def __init__(self, sender):
    self.__sender__ = sender
    self.__job_uuid__ = uuid4().bytes

  def get_job_uuid(self):
    return self.__job_uuid__

  def get_sender(self):
    return self.__sender__

class UUIDCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(UUIDCommand, self).__init__(*args, **kwargs)
    self.__uuid__ = kwargs.get('uuid')
    if not self.__uuid__:
      raise ValueError('The value of uuid must be a valid UUID.')

  def get_uuid(self):
    return self.__uuid__

class AnswerCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(AnswerCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'uuid_answer %s' % self.__uuid__

class BreakCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(BreakCommand, self).__init__(*args, **kwargs)
    self.__stop_all__ = kwargs.get('all', default = False)

  def __str__(self):
    if not self.__stop_all__:
      return 'uuid_break %s' % self.__uuid__
    else:
      return 'uuid_break %s all' % self.__uuid__

class BridgeCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(BridgeCommand, self).__init__(*args, **kwargs)
    self.__other_uuid__ = kwargs.get('other_uuid')
    if not self.__other_uuid__:
      raise ValueError('The value of other_uuid must be a valid UUID.')

  def __str__(self):
    return 'uuid_bridge %s %s' % (self.__uuid__, self.__other_uuid__)

class BroadcastCommand(UUIDCommand):
  pass

class GetAudioLevelCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(GetAudioLevelCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'uuid_audio %s start read level' % self.__uuid__

class OriginateCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(OriginateCommand, self).__init__(*args, **kwargs)
    self.__url__ = kwargs.get('url')
    self.__extension__ = kwargs.get('extension')
    self.__app_name__ = kwargs.get('app_name')
    self.__app_args__ = kwargs.get('app_args', default = [])
    if not isinstance(self.__app_args__, list):
      raise TypeError('The app_args parameter must be a list type.')
    self.__options__ = kwargs.get('options', default = [])
    if not isinstance(self.__options__, list):
      raise TypeError('The options parameter must be a list type.')

  def get_app_name(self):
    return self.__app_name__

  def get_app_args(self):
    return self.__app_args__

  def get_extension(self):
    return self.__extension__

  def get_options(self):
    return self.__options__

  def get_url(self):
    return self.__url__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi originate ')
    if self.__options__:
      buffer.write('{%s}' % ','.join(self.__options__))
    buffer.write('%s ' % self.__url__)
    if self.__extension__:
      buffer.write('%s' % self.__extension__)
    else:
      buffer.write('&%s(%s)' % (self.__app_name__,
        ' '.join(self.__app_args__)))
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class PauseCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(PauseCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'pause %s on' % self.__uuid__

class SetAudioLevelCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(SetAudioLevelCommand, self).__init__(*args, **kwargs)
    self.__audio_level__ = kwargs.get('level')
    if not self.__audio_level__ or self.__audio_level__ < -4.0 or \
      self.__audio_level__ > 4.0:
    raise ValueError('The level value %s is invalid.' % self.__audio_level__)

  def __str__(self):
    return 'uuid_audio %s start write level %i' % (self.__uuid__,
      self.__audio_level__)

class UnpauseCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(UnpauseCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'pause %s off' % self.__uuid__

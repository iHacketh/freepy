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
    self.__job_uuid__ = uuid4().get_urn().split(':', 2)[2]

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
    return 'bgapi uuid_answer %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class BreakCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(BreakCommand, self).__init__(*args, **kwargs)
    self.__stop_all__ = kwargs.get('all', default = False)

  def stop_all(self):
    return self.__stop_all__

  def __str__(self):
    if not self.__stop_all__:
      return 'bgapi uuid_break %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__job_uuid__)
    else:
      return 'bgapi uuid_break %s all\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__job_uuid__)

class BridgeCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(BridgeCommand, self).__init__(*args, **kwargs)
    self.__other_uuid__ = kwargs.get('other_uuid')
    if not self.__other_uuid__:
      raise ValueError('The value of other_uuid must be a valid UUID.')

  def get_other_uuid(self):
    return self.__other_uuid__

  def __str__(self):
    return 'bgapi uuid_bridge %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__other_uuid__, self.__job_uuid__)

class BroadcastCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(BroadcastCommand, self).__init__(*args, **kwargs)
    self.__leg__ = kwargs.get('leg')
    if not self.__leg__ or not self.__leg__ == 'aleg' or \
      not self.__leg__ == 'bleg' or not self.__leg__ == 'both':
      raise ValueError('The leg value %s is invalid' % self.__leg__)
    self.__path__ = kwargs.get('path')
    self.__app_name__ = kwargs.get('app_name')
    self.__app_args__ = kwargs.get('app_args')
    if self.__path__ and self.__app_name__:
      raise RuntimeError('A broadcast command can specify either a path \
      or an app_name but not both.')

  def get_leg(self):
    return self.__leg__

  def get_path(self):
    return self.__path__

  def get_app_name(self):
    return self.__app_name__

  def get_app_args(self):
    return self.__app_args__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi uuid_broadcast %s ' % self.__uuid__)
    if self.__path__:
      buffer.write('%s ' % self.__path__)
    else:
      buffer.write('%s::%s ' % (self.__app_name__, self.__app_args__))
    buffer.write('%s\nJob-UUID: %s\n\n' % self.__leg__, self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class ChatCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(ChatCommand, self).__init__(*args, **kwargs)
    self.__text__ = kwargs.get('text', default = '')

  def get_text(self):
    return self.__text__

  def __str__(self):
    return 'bgapi uuid_chat %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__text__, self.__job_uuid__)

class DeflectCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(DeflectCommand, self).__init__(*args, **kwargs)
    self.__url__ = kwargs.get('url')

  def get_url(self):
    return self.__url__

  def __str__(self):
    return 'bgapi uuid_deflect %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__url__, self.__job_uuid__)

class DisplayCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(DisplayCommand, self).__init__(*args, **kwargs)
    self.__display__ = kwargs.get('display')

    def get_display(self):
      return self.__display__

  def __str__(self):
    return 'bgapi uuid_display %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__display__, self.__job_uuid__)

class DualTransferCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(DualTransferCommand, self).__init__(*args, **kwargs)
    self.__extension_a__ = kwargs.get('extension_a')
    self.__extension_b__ = kwargs.get('extension_b')
    self.__dialplan_a__ = kwargs.get('dialplan_a')
    self.__dialplan_b__ = kwargs.get('dialplan_b')
    self.__context_a__ = kwargs.get('context_a')
    self.__context_b__ = kwargs.get('context_b')
    if not self.__extension_a__ or not self.__extension_b__:
      raise RuntimeError('A dual transer command requires the extension_a \
        and extension_b parameters to be provided.')

  def get_extension_a(self):
    return self.__extension_a__

  def get_extension_b(self):
    return self.__extension_b__

  def get_dialplan_a(self):
    return self.__dialplan_a__

  def get_dialplan_b(self):
    return self.__dialplan_b__

  def get_context_a(self):
    return self.__context_a__

  def get_context_b(self):
    return self.__context_b__

  def __str__(self):
    buffer = StringIO()
    buffer.write(self.__extension_a__)
    if self.__dialplan_a__:
      buffer.write('/%s' % self.__dialplan_a__)
    if self.__context_a__:
      buffer.write('/%s' % self.__context_a__)
    destination_a = buffer.getvalue()
    buffer.seek(0)
    buffer.write(self.__extension_b__)
    if self.__dialplan_b__:
      buffer.write('/%s' % self.__dialplan_b__)
    if self.__context_b__:
      buffer.write('/%s' % self.__context_b__)
    destination_b = buffer.getvalue()
    buffer.close()
    return 'bgapi uuid_dual_transfer %s %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      destination_a, destination_b, self.__job_uuid__)

class DumpCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(DumpCommand, self).__init__(*args, **kwargs)
    self.__format__ = kwargs.get('format', default = 'XML')

  def get_format(self):
    return self.__format__

  def __str__(self):
    return 'bgapi uuid_dump %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__format__, self.__job_uuid__)

class EarlyOkayCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(EarlyOkayCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_early_ok %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class FileManagerCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(FileManagerCommand, self).__init__(*args, **kwargs)
    self.__command__ = kwargs.get('command')
    if not self.__command__ or not self.__command__ == 'speed' and \
      not self.__command__ == 'volume' and not self.__command__ == 'pause' and \
      not self.__command__ == 'stop' and not self.__command__ == 'truncate' and \
      not self.__command__ == 'restart' and not self.__command__ == 'seek':
      raise ValueError('The command parameter %s is invalid.' % self.__command__)
    self.__value__ = kwargs.get('value')

  def get_command(self):
    return self.__command__

  def get_value(self):
    return self.__value__

  def __str__(self):
    if self.__value__:
      return 'bgapi uuid_fileman %s %s:%s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__command__, self.__value__, self.__job_uuid__)
    else:
      return 'bgapi uuid_fileman %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__command__, self.__job_uuid__)

class FlushDTMFCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(FlushDTMFCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_flush_dtmf %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class GetAudioLevelCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(GetAudioLevelCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_audio %s start read level\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class GetBugListCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(GetBugListCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_buglist %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class GetVariableCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(GetVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    if not self.__name__:
      raise ValueError('The name parameter %s is invalid.' % self.__name__)

  def get_name(self):
    return self.__name__

  def __str__(self):
    return 'bgapi uuid_getvar %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__name__, self.__job_uuid__)

class HoldCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(HoldCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_hold %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class KillCommand(UUIDCommand):
  pass

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
    if self.__extension__ and self.__app_name__:
      raise RuntimeError('An originate command can specify either an \
      extension or an app_name but not both.')

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
    buffer.write('\nJob-UUID: %s\n\n' % self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class PauseCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(PauseCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi pause %s on\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class SetAudioLevelCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(SetAudioLevelCommand, self).__init__(*args, **kwargs)
    self.__audio_level__ = kwargs.get('level')
    if not self.__audio_level__ or self.__audio_level__ < -4.0 or \
      self.__audio_level__ > 4.0:
      raise ValueError('The level value %s is invalid.' % self.__audio_level__)

  def get_level(self):
    return self.__audio_level__

  def __str__(self):
    return 'bgapi uuid_audio %s start write level %f\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__audio_level__, self.__job_uuid__)

class StartDebugMediaCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(StartDebugMediaCommand, self).__init__(*args, **kwargs)
    self.__option__ = kwargs.get('option')

  def get_option(self):
    return self.__option__

  def __str__(self):
    return 'bgapi uuid_debug_media %s %s on\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__option__, self.__job_uuid__)

class StartDisplaceCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(StartDisplaceCommand, self).__init__(*args, **kwargs)
    self.__path__ = kwargs.get('path')
    self.__limit__ = kwargs.get('limit')
    self.__mux__ = kwargs.get('mux')

  def get_limit(self):
    return self.__limit__

  def get_mux(self):
    return self.__mux__

  def get_path(self):
    return self.__path__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi uuid_displace %s start %s' % (self.__uuid__,
      self.__path__))
    if self.__limit__:
      buffer.write(' %i' % self.__limit__)
    if self.__mux__:
      buffer.write(' mux')
    buffer.write('\nJob-UUID: %s\n\n' % self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class StatusCommand(BackgroundCommand):
  def __str__(self):
    return 'bgapi status\nJob-UUID: %s\n\n' % self.__job_uuid__

class StopDebugMediaCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(StopDebugMediaCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_debug_media %s off\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class StopDisplaceCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(StopDisplaceCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_displace %s stop\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class UnholdCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(UnholdCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_hold off %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class UnpauseCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(UnpauseCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi pause %s off\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

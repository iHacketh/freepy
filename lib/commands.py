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

class ACLCheckCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(ACLCommand, self).__init__(*args, **kwargs)
    self.__ip__ = kwargs.get('ip')
    self.__list_name__ = kwargs.get('list_name')

  def get_ip(self):
    return self.__ip__

  def get_list_name(self):
    return self.__list_name__

  def __str__(self):
    return 'bgapi acl %s %s\nJob-UUID: %s\n\n' % (self.__ip__,
      self.__list_name__, self.__job_uuid__)

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

class CheckUserGroupCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(CheckUserGroupCommand, self).__init__(*args, **kwargs)
    self.__user__ = kwargs.get('user')
    self.__domain__ = kwargs.get('domain')
    self.__group_name__ = kwargs.get('group_name')

  def get_domain(self):
    return self.__domain__

  def get_group_name(self):
    return self.__group_name__

  def get_user(self):
    return self.__user__

  def __str__(self):
    if not self.__domain__:
      return 'bgapi in_group %s %s\nJob-UUID: %s\n\n' % (self.__user__,
        self.__group_name__, self.__job_uuid__)
    else:
      return 'bgapi in_group %s@%s %s\nJob-UUID: %s\n\n' % (self.__user__,
        self.__domain__, self.__group_name__, self.__job_uuid__)

class DeflectCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(DeflectCommand, self).__init__(*args, **kwargs)
    self.__url__ = kwargs.get('url')

  def get_url(self):
    return self.__url__

  def __str__(self):
    return 'bgapi uuid_deflect %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__url__, self.__job_uuid__)

class DialedExtensionHupAllCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(DialedExtensionHupAllCommand, self).__init__(*args, **kwargs)
    self.__clearing__ = kwargs.get('clearing')
    self.__extension__ = kwargs.get('extension')

  def get_clearing(self):
    return self.__clearing__

  def get_extension(self):
    return self.__extension__

  def __str__(self):
    return 'bgapi fsctl hupall %s dialed_ext %s\nJob-UUID: %s\n\n' % (self.__clearing__,
      self.__extension__, self.__job_uuid__)

class DisableMediaCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(DisableMediaCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_media off %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class DisableVerboseEventsCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(DisableVerboseEventsCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl verbose_events off\nJob-UUID: %s\n\n' % self.__job_uuid__

class DisplayCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(DisplayCommand, self).__init__(*args, **kwargs)
    self.__display__ = kwargs.get('display')

    def get_display(self):
      return self.__display__

  def __str__(self):
    return 'bgapi uuid_display %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__display__, self.__job_uuid__)

class DomainExistsCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(DomainExistsCommand, self).__init__(*args, **kwargs)
    self.__domain__ = kwargs.get('domain')

  def get_domain(self):
    return self.__domain__

  def __str__(self):
    return 'bgapi domain_exists %s\nJob-UUID: %s\n\n' % (self.__domain__,
      self.__job_uuid__)

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

class EnableMediaCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(EnableMediaCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_media %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class EnableSessionHeartbeatCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(EnableSessionHeartbeatCommand, self).__init__(*args, **kwargs)
    self.__start_time__ = kwargs.get('start_time') # Seconds in the future to start

  def get_start_time(self):
    return self.__start_time__

  def __str__(self):
    if not self.__start_time__:
      return 'bgapi uuid_session_heartbeat %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__job_uuid__)
    else:
      return 'bgapi uuid_session_heartbeat %s sched %i\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__start_time__, self.__job_uuid__)

class EnableVerboseEventsCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(EnableVerboseEventsCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl verbose_events on\nJob-UUID: %s\n\n' % self.__job_uuid__

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

class GetDefaultDTMFDurationCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(GetDefaultDTMFDurationCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl default_dtmf_duration 0\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetGlobalVariableCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(GetGlobalVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    if not self.__name__:
      raise ValueError('The name parameter is required.')

  def get_name(self):
    return self.__name__

  def __str__(self):
    return 'bgapi global_getvar %s\nJob-UUID: %s\n\n' % (self.__name__,
      self.__job_uuid__)

class GetMaxSessionsCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(GetMaxSessionsCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl max_sessions\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetMaximumDTMFDurationCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(GetMaximumDTMFDurationCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl max_dtmf_duration 0\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetMinimumDTMFDurationCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(GetMinimumDTMFDurationCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl min_dtmf_duration 0\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetSessionsPerSecondCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(GetSessionsPerSecondCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl last_sps\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetVariableCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(GetVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    if not self.__name__:
      raise ValueError('The name parameter is requied.')

  def get_name(self):
    return self.__name__

  def __str__(self):
    return 'bgapi uuid_getvar %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__name__, self.__job_uuid__)

class GetGroupCallBridgeStringCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(GetGroupCallBridgeStringCommand, self).__init__(*args, **kwargs)
    self.__group__ = kwargs.get('group')
    self.__domain__ = kwargs.get('domain')
    self.__option__ = kwargs.get('option')
    if self.__option__ and not self.__option__ == '+F' and \
      not self.__option__ == '+A' and not self.__option__ == '+E':
      raise ValueError('The option parameter %s is invalid.' % self.__option__)

  def get_domain(self):
    return self.__domain__

  def get_group(self):
    return self.__group__

  def get_option(self):
    return self.__option__

  def __str__(self):
    if not self.__option__:
      return 'bgapi group_call %s@%s\nJob-UUID: %s\n\n' % (self.__group__,
        self.__domain__, self.__job_uuid__)
    else:
      return 'bgapi group_call %s@%s%s\nJob-UUID: %s\n\n' % (self.__group__,
        self.__domain__, self.__option__, self.__job_uuid__)

class HoldCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(HoldCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_hold %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class HupAllCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(HupAllCommand, self).__init__(*args, **kwargs)
    self.__cause__ = kwargs.get('cause')
    self.__var_name__ = kwargs.get('var_name')
    self.__var_value__ = kwargs.get('var_value')

  def get_cause(self):
    return self.__cause__

  def get_variable_name(self):
    return self.__var_name__

  def get_variable_value(self):
    return self.__var_value__

  def __str__(self):
    if self.__var_name__ and self.__var_value__:
      return 'bgapi hupall %s %s %s\nJob-UUID: %s\n\n' % (self.__cause__,
        self.__var_name__, self.__var_value__, self.__job_uuid__)
    else:
      return 'bgapi hupall %s\nJob-UUID: %s\n\n' % (self.__cause__,
        self.__job_uuid__)

class KillCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(KillCommand, self).__init__(*args, **kwargs)
    self.__cause__ = kwargs.get('cause')

  def get_cause(self):
    return self.__cause__

  def __str__(self):
    if not self.__cause__:
      return 'bgapi uuid_kill %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__job_uuid__)
    else:
      return 'bgapi uuid_kill %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__cause__, self.__job_uuid__)

class LimitCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(LimitCommand, self).__init__(*args, **kwargs)
    self.__backend__ = kwargs.get('backend')
    self.__realm__ = kwargs.get('realm')
    self.__resource__ = kwargs.get('resource')
    self.__max_calls__ = kwargs.get('max_calls')
    self.__interval__ = kwargs.get('interval')
    self.__number__ = kwargs.get('number')
    self.__dialplan__ = kwargs.get('dialplan')
    self.__context__ = kwargs.get('context')

  def get_backend(self):
    return self.__backend__

  def get_realm(self):
    return self.__realm__

  def get_resource(self):
    return self.__resource__

  def get_max_calls(self):
    return self.__max_calls__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi uuid_limit %s %s %s %s' % (self.__uuid__,
      self.__backend__, self.__realm__, self.__resource__))
    if self.__max_calls__:
      buffer.write(' %i' % self.__max_calls__)
      if self.__interval__:
        buffer.write('/%i' % self.__interval__)
    if self.__number__:
      buffer.write(' %s' % self.__number__)
      if self.__dialplan__:
        buffer.write(' %s' % self.__dialplan__)
        if self.__context__:
          buffer.write(' %s' % self.__context__)
    buffer.write('\nJob-UUID: %s\n\n' % self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

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

class ParkCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(ParkCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_park %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class PauseCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(PauseCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi pause %s on\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class PauseSessionCreationCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(PauseSessionCreationCommand, self).__init__(*args, **kwargs)
    self.__direction__ = kwargs.get('direction')

  def get_direction(self):
    return self.__direction__

  def __str__(self):
    if not self.__direction__:
      return 'bgapi fsctl pause\nJob-UUID: %s\n\n' % self.__job_uuid__
    else:
      return 'bgapi fsctl pause %s\nJob-UUID: %s\n\n' % (self.__direction__,
        self.__job_uuid__)

class PreAnswerCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(PreAnswerCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_preanswer %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class PreProcessCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(PreProcessCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_preprocess %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class ReceiveDTMFCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(ReceiveDTMFCommand, self).__init__(*args, **kwargs)
    self.__digits__ = kwargs.get('digits')
    self.__duration__ = kwargs.get('tone_duration')

  def get_digits(self):
    return self.__digits__

  def get_tone_duration(self):
    return self.__duration__

  def __str__(self):
    if not self.__duration__:
      return 'bgapi uuid_recv_dtmf %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__digits__, self.__job_uuid__)
    else:
      return 'bgapi uuid_recv_dtmf %s %s@%i\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__digits__, self.__duration__, self.__job_uuid__)

class ReclaimMemoryCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(ReclaimMemoryCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl reclaim_mem\nJob-UUID: %s\n\n' % self.__job_uuid__

class RenegotiateMediaCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(RenegotiateMediaCommand, self).__init__(*args, **kwargs)
    self.__codec__ = kwargs.get('codec')

  def get_codec(self):
    return self.__codec__

  def __str__(self):
    return 'bgapi uuid_media_reneg %s =%s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__codec__, self.__job_uuid__)

class ResumeSessionCreationCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(ResumeSessionCreationCommand, self).__init__(*args, **kwargs)
    self.__direction__ = kwargs.get('direction')

  def get_direction(self):
    return self.__direction__

  def __str__(self):
    if not self.__direction__:
      return 'bgapi fsctl resume\nJob-UUID: %s\n\n' % self.__job_uuid__
    else:
      return 'bgapi fsctl resume %s\nJob-UUID: %s\n\n' % (self.__direction__,
        self.__job_uuid__)

class SendDTMFCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(SendDTMFCommand, self).__init__(*args, **kwargs)
    self.__digits__ = kwargs.get('digits')
    self.__duration__ = kwargs.get('tone_duration')

  def get_digits(self):
    return self.__digits__

  def get_tone_duration(self):
    return self.__duration__

  def __str__(self):
    if not self.__duration__:
      return 'bgapi uuid_send_dtmf %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__digits__, self.__job_uuid__)
    else:
      return 'bgapi uuid_send_dtmf %s %s@%i\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__digits__, self.__duration__, self.__job_uuid__)

class SendInfoCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(SendInfoCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_send_info %s\nJob-UUID: %s\n\n' % (self.__uuid__,
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

class SetDefaultDTMFDurationCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(SetDefaultDTMFDurationCommand, self).__init__(*args, **kwargs)
    self.__duration__ = kwargs.get('duration')

  def get_duration(self):
    return self.__duration__

  def __str__(self):
    return 'bgapi fsctl default_dtmf_duration %i\nJob-UUID: %s\n\n' % (self.__duration__,
      self.__job_uuid__)

class SetGlobalVariableCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(SetGlobalVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    self.__value__ = kwargs.get('value')
    if not self.__name__ or not self.__value__:
      raise RuntimeError('The set global variable command requires both name \
      and value parameters.')

  def get_name(self):
    return self.__name__

  def get_value(self):
    return self.__value__

  def __str__(self):
    return 'bgapi global_setvar %s=%s\nJob-UUID: %s\n\n' % (self.__name__,
      self.__value__, self.__job_uuid__)

class SetMaximumDTMFDurationCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(SetMaximumDTMFDurationCommand, self).__init__(*args, **kwargs)
    self.__duration__ = kwargs.get('duration')

  def get_duration(self):
    return self.__duration__

  def __str__(self):
    return 'bgapi fsctl max_dtmf_duration %i\nJob-UUID: %s\n\n' % (self.__duration__,
      self.__job_uuid__)

class SetMinimumDTMFDurationCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(SetMinimumDTMFDurationCommand, self).__init__(*args, **kwargs)
    self.__duration__ = kwargs.get('duration')

  def get_duration(self):
    return self.__duration__

  def __str__(self):
    return 'bgapi fsctl min_dtmf_duration %i\nJob-UUID: %s\n\n' % (self.__duration__,
      self.__job_uuid__)

class SetMultipleVariableCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(SetMultipleVariableCommand, self).__init__(*args, **kwargs)
    self.__variables__ = kwargs.get('variables')
    if not isinstance(self.__variables__, dict):
      raise TypeError('The variables parameter must be of type dict.')
    variable_list = list()
    for key, value in self.__variables__:
      variable_list.append('%s=%s' % (key, value))
    self.__variables_string__ = ';'.join(variable_list)


  def __str__(self):
    return 'bgapi uuid_setvar_multi %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__variables_string__, self.__job_uuid__)

class SetSessionsPerSecondCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(SetSessionsPerSecondCommand, self).__init__(*args, **kwargs)
    self.__sessions_per_second__ = kwargs.get('sessions_per_second')

  def get_sessions_per_second(self):
    return self.__sessions_per_second__

  def __str__(self):
    return 'bgapi fsctl sps %i\nJob-UUID: %s\n\n' % (self.__sessions_per_second__,
      self.__job_uuid__)

class SetVariableCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(SetVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    self.__value__ = kwargs.get('value')
    if not self.__name__ or not self.__value__:
      raise RuntimeError('The set variable command requires both name \
      and value parameters.')

  def get_name(self):
    return self.__name__

  def get_value(self):
    return self.__value__

  def __str__(self):
    return 'bgapi uuid_setvar %s %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__name__, self.__value__, self.__job_uuid__)

class ShutdownCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(ShutdownCommand, self).__init__(*args, **kwargs)
    self.__option__ = kwargs.get('option')
    if self.__option__ and not self.__option__ == 'cancel' and \
      not self.__option__ == 'elegant' and not self.__option__ == 'asap' and \
      not self.__option__ == 'restart':
      raise ValueError('The option %s is an invalid option.' % self.__option__)

  def get_option(self):
    return self.__option__

  def __str__(self):
    if not self.__option__:
      return 'bgapi fsctl shutdown\nJob-UUID: %s\n\n' % self.__job_uuid__
    else:
      return 'bgapi fsctl shutdown %s\nJob-UUID: %s\n\n' % (self.__option__,
        self.__job_uuid__)

class SimplifyCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(SimplifyCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_simplify %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

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
  def __init__(self, *args, **kwargs):
    super(StatusCommand, self).__init__(*args, **kwargs)

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

class SyncClockCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(SyncClockCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl sync_clock\nJob-UUID: %s\n\n' % self.__job_uuid__

class SyncClockWhenIdleCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(SyncClockWhenIdleCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl sync_clock_when_idle\nJob-UUID: %s\n\n' % self.__job_uuid__

class TransferCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(TransferCommand, self).__init__(*args, **kwargs)
    self.__leg__ = kwargs.get('leg')
    self.__extension__ = kwargs.get('extension')
    self.__dialplan__ = kwargs.get('dialplan')
    self.__context__ = kwargs.get('context')

  def get_context(self):
    return self.__context__

  def get_dialplan(self):
    return self.__dialplan__

  def get_extension(self):
    return self.__extension__

  def get_leg(self):
    return self.__leg__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi uuid_transfer %s' % self.__uuid__)
    if self.__leg__:
      buffer.write(' %s' % self.__leg__)
    buffer.write(' %s' % self.__extension__)
    if self.__dialplan__:
      buffer.write(' %s' % self.__dialplan__)
    if self.__context__:
      buffer.write(' %s' % self.__context__)
    buffer.write('\nJob-UUID: %s\n\n' % self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

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

class UnsetVariableCommand(UUIDCommand):
  def __init__(self, *args, **kwargs):
    super(UnsetVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    if not self.__name__:
      raise RuntimeError('The unset variable commands requires the name \
      parameter.')

  def get_name(self):
    return self.__name__

  def __str__(self):
    return 'bgapi uuid_setvar %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__name__, self.__job_uuid__)

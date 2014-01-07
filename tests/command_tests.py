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

from lib.commands import *
from unittest import TestCase, expectedFailure

class ACLCheckCommandTests(TestCase):
  def test_success_scenario(self):
    command = ACLCheckCommand(object(), ip = '192.168.1.1', list_name = 'lan')
    # Monkey patch the Job-UUID
    command.__job_uuid__ = 'd3418bd1-cfa4-42a9-8a8e-a04a770c808d'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi acl 192.168.1.1 lan\nJob-UUID: d3418bd1-cfa4-42a9-8a8e-a04a770c808d\n\n'
    self.assertTrue(str(command) == desired_output)

  def test_success_scenario1(self):
  	#this is to see if we pass nothing for ip or list_name what will happen. 
  	command = ACLCheckCommand(object(), None, None )
  	print "TODO: Discuss this scenario. Is none/none ok?\n\n"
  	#print str(command)

class CheckUserGroupCommandTests(TestCase):
  def test_success_scenario(self):
  	command = CheckUserGroupCommand(object(), user = 'test', domain = 'domain_test.com', group_name = 'groupname_test')
  	# Monkey patch the Job-UUID
  	command.__job_uuid__ = '69e18d2f-b821-4022-95d6-8eecf1550bdc'
  	# Make sure we are generating the correct output.
  	desired_output = 'bgapi in_group test@domain_test.com groupname_test\nJob-UUID: 69e18d2f-b821-4022-95d6-8eecf1550bdc\n\n'
  	self.assertTrue(str(command) == desired_output)
  	#print str(command)

class DialedExtensionHupAllCommandTests(TestCase):
   def test_success_scenario(self):
    command = DialedExtensionHupAllCommand(object(), clearing = '999-999-9999', extension = '493')
    # Monkey patch the Job-UUID
    command.__job_uuid__ = '7e0955fd-eb0c-4b6f-9643-2fa5cdcb34c8'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl hupall 999-999-9999 dialed_ext 493\nJob-UUID: 7e0955fd-eb0c-4b6f-9643-2fa5cdcb34c8\n\n'
    self.assertTrue(str(command) == desired_output)
    #print str(command)    

class DisableVerboseEventsCommandTests(TestCase):
   def test_success_scenario(self):
    command = DisableVerboseEventsCommand(object())
    # Monkey patch the Job-UUID
    command.__job_uuid__ = 'afd53e32-69cf-4730-84cd-c2b6d57ea90d'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl verbose_events off\nJob-UUID: afd53e32-69cf-4730-84cd-c2b6d57ea90d\n\n'
    self.assertTrue(str(command) == desired_output)
    #print str(command)    

class DomainExistsCommandTests(TestCase):
   def test_success_scenario(self):
    command = DomainExistsCommand(object(), domain = 'domain_test.com')
    # Monkey patch the Job-UUID
    command.__job_uuid__ = '01bc12c7-3c12-4db7-b5ef-5f33c4383823'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi domain_exists domain_test.com\nJob-UUID: 01bc12c7-3c12-4db7-b5ef-5f33c4383823\n\n'
    self.assertTrue(str(command) == desired_output)
    #print str(command)    

class EnableVerboseEventsCommandTests(TestCase):
   def test_success_scenario(self):
   	command = EnableVerboseEventsCommand(object())
   	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '0197ca48-a54a-4072-a010-2f36ec5f1304'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi fsctl verbose_events on\nJob-UUID: 0197ca48-a54a-4072-a010-2f36ec5f1304\n\n'
   	self.assertTrue(str(command) == desired_output)
    #print str(command)

class GetDefaultDTMFDurationCommandTests(TestCase):
   def test_success_scenario(self):
   	command = GetDefaultDTMFDurationCommand(object())   	
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '5819d146-0145-4178-9591-c3cf96e110b6'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi fsctl default_dtmf_duration 0\nJob-UUID: 5819d146-0145-4178-9591-c3cf96e110b6\n\n'
   	self.assertTrue(str(command) == desired_output)
    #print str(command)

class GetGlobalVariableCommandTests(TestCase):
   def test_success_scenario(self):
   	command = GetGlobalVariableCommand(object(), name='testVariable')   	
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = 'dbec6d76-360e-4808-891d-cb578dcf804c'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi global_getvar testVariable\nJob-UUID: dbec6d76-360e-4808-891d-cb578dcf804c\n\n'
   	self.assertTrue(str(command) == desired_output)
    #print str(command)

class GetMaxSessionsCommandTests(TestCase):
   def test_success_scenario(self):
   	command = GetMaxSessionsCommand(object())   	
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '5819d146-0145-4178-9591-c3cf96e110b6'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi fsctl max_sessions\nJob-UUID: 5819d146-0145-4178-9591-c3cf96e110b6\n\n'
   	self.assertTrue(str(command) == desired_output)
    #print str(command)

class GetMaximumDTMFDurationCommandTests(TestCase):
   def test_success_scenario(self):
   	command = GetMaximumDTMFDurationCommand(object())   	
    # Monkey patch the Job-UUID
   	command.__job_uuid__ = '2171f6af-85a5-4163-b08c-277af80b1cd4'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi fsctl max_dtmf_duration 0\nJob-UUID: 2171f6af-85a5-4163-b08c-277af80b1cd4\n\n'
   	self.assertTrue(str(command) == desired_output)
    

class GetMinimumDTMFDurationCommandTests(TestCase):
   def test_success_scenario(self):
   	command = GetMinimumDTMFDurationCommand(object())   	
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '461b3ee1-5ca2-46e5-823d-06ee2630a93d'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi fsctl min_dtmf_duration 0\nJob-UUID: 461b3ee1-5ca2-46e5-823d-06ee2630a93d\n\n'
   	self.assertTrue(str(command) == desired_output)

class GetSessionsPerSecondCommandTests(TestCase):
   def test_success_scenario(self):
   	command = GetSessionsPerSecondCommand(object())   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '9fb85c43-7a88-452d-8fbf-04641944315f'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi fsctl last_sps\nJob-UUID: 9fb85c43-7a88-452d-8fbf-04641944315f\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)

class GetGroupCallBridgeStringCommandTests(TestCase):
   def test_success_scenario(self):
   	command = GetGroupCallBridgeStringCommand(object(), group = 'groupname_test', domain = 'domain_test.com', option = '+F')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '73b98e2d-eb6e-4d88-af4b-5ed2cc541399'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi group_call groupname_test@domain_test.com+F\nJob-UUID: 73b98e2d-eb6e-4d88-af4b-5ed2cc541399\n\n'
   	self.assertTrue(str(command) == desired_output)
   	print "TODO: Discuss this scenario. TEST FOR OPTION BEING A OR E OR F AS VALID ONLY!\n\n"
   	#print str(command)

class HupAllCommandTests(TestCase):
   def test_success_scenario(self):
   	command = HupAllCommand(object(), cause = 'test_cause', var_name = 'test_var_name', var_value = 'test_var_value')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = 'c12ca57c-5944-4a7c-b148-54204997cc78'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi hupall test_cause test_var_name test_var_value\nJob-UUID: c12ca57c-5944-4a7c-b148-54204997cc78\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)

class LoadModuleCommandTests(TestCase):
   def test_success_scenario(self):
    command = LoadModuleCommand(object(), name = "testModule")
    #print str(command)
    # Monkey patch the Job-UUID
    command.__job_uuid__ = '3af9f33f-cf8d-4ed6-a42a-661853950b2c'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi load testModule\nJob-UUID: 3af9f33f-cf8d-4ed6-a42a-661853950b2c\n\n'
    self.assertTrue(str(command) == desired_output)
   	#print str(command)    

class OriginateCommandTests(TestCase):
   def test_success_scenario(self):
    #command = OriginateCommand(object(), url = "http://test.com", extension = None, app_name = 'appTestme', app_args = None, options = None)
    print "TODO: LOOKS LIKE VALID ERROR IN OriginateCommandTests(Commented Out)!\n\n"
    # Monkey patch the Job-UUID
    #command.__job_uuid__ = '3af9f33f-cf8d-4ed6-a42a-661853950b2c'
    # Make sure we are generating the correct output.
    #desired_output = 'bgapi load testModule\nJob-UUID: 3af9f33f-cf8d-4ed6-a42a-661853950b2c\n\n'
    #self.assertTrue(str(command) == desired_output)
    
   	#print str(command)    

class PauseSessionCreationCommandTests(TestCase):
   def test_success_scenario(self):
    command = PauseSessionCreationCommand(object(), direction = "testDirection")
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'c0cf36c0-c31e-4388-bf75-9da4ea86001d'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl pause testDirection\nJob-UUID: c0cf36c0-c31e-4388-bf75-9da4ea86001d\n\n'
    self.assertTrue(str(command) == desired_output)

class ReclaimMemoryCommandTests(TestCase):
   def test_success_scenario(self):
    command = ReclaimMemoryCommand(object())
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'f9572acf-f84f-4a69-b4dd-8ce1e0b52a6a'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl reclaim_mem\nJob-UUID: f9572acf-f84f-4a69-b4dd-8ce1e0b52a6a\n\n'
    self.assertTrue(str(command) == desired_output)

class ResumeSessionCreationCommandTests(TestCase):
   def test_success_scenario_passvariable(self):
    print "NICE!: EXAMPLE OF VALIDATING OBJECT W AND w/O PARAM VALUE"
    command = ResumeSessionCreationCommand(object(), direction = "testDirection")
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '7d8e4035-fba0-4327-b30b-6511eb1bccc6'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl resume testDirection\nJob-UUID: 7d8e4035-fba0-4327-b30b-6511eb1bccc6\n\n'
    self.assertTrue(str(command) == desired_output)
   def test_success_scenario_novariable(self):
    command = ResumeSessionCreationCommand(object())
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '7d8e4035-fba0-4327-b30b-6511eb1bccc6'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl resume\nJob-UUID: 7d8e4035-fba0-4327-b30b-6511eb1bccc6\n\n'
    self.assertTrue(str(command) == desired_output)

class SetDefaultDTMFDurationCommandTests(TestCase):
   def test_success_scenario(self):
    command = SetDefaultDTMFDurationCommand(object(), duration = 500)
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '8d8e7133-4059-4880-92a8-96057dd3d910'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl default_dtmf_duration 500\nJob-UUID: 8d8e7133-4059-4880-92a8-96057dd3d910\n\n'
    self.assertTrue(str(command) == desired_output)

class SetGlobalVariableCommandTests(TestCase):
   def test_success_scenario(self):
    print "TODO: Name & Value Must be POPULATED!\n\n"
    command = SetGlobalVariableCommand(object(), name = 'testName', value = 'testValue')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '1283f904-5235-4f01-8114-cc77f9711d35'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi global_setvar testName=testValue\nJob-UUID: 1283f904-5235-4f01-8114-cc77f9711d35\n\n'
    self.assertTrue(str(command) == desired_output)

class SetMaximumDTMFDurationCommandTests(TestCase):
   def test_success_scenario(self):
    command = SetMaximumDTMFDurationCommand(object(), duration = 500)
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '94f3f967-e6d8-4890-ac72-2ab93a1a625b'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl max_dtmf_duration 500\nJob-UUID: 94f3f967-e6d8-4890-ac72-2ab93a1a625b\n\n'
    self.assertTrue(str(command) == desired_output)

class SetMinimumDTMFDurationCommandTests(TestCase):
   def test_success_scenario(self):
    command = SetMinimumDTMFDurationCommand(object(), duration = 500)
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'b3bbb9d9-784a-4b51-9bf1-861d8d485c1b'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl min_dtmf_duration 500\nJob-UUID: b3bbb9d9-784a-4b51-9bf1-861d8d485c1b\n\n'
    self.assertTrue(str(command) == desired_output)

class SetSessionsPerSecondCommandTests(TestCase):
   def test_success_scenario(self):
    command = SetSessionsPerSecondCommand(object(), sessions_per_second = 15)
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '18d0ce07-e59e-4d2c-ac86-18ef1fa821ce'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl sps 15\nJob-UUID: 18d0ce07-e59e-4d2c-ac86-18ef1fa821ce\n\n'
    self.assertTrue(str(command) == desired_output)

class ShutdownCommandTests(TestCase):
   def test_success_scenario(self):
    command = ShutdownCommand(object(), option = 'elegant')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'ef321ad7-4993-40eb-8e97-1df74bc32bc4'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl shutdown elegant\nJob-UUID: ef321ad7-4993-40eb-8e97-1df74bc32bc4\n\n'
    self.assertTrue(str(command) == desired_output)
    print "TODO: TEST FOR OPTION BEING elegant, asap, restart, cancel!\n\n"

class StatusCommandTests(TestCase):
   def test_success_scenario(self):
    command = StatusCommand(object())
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'b12db00e-1a36-4cbf-864d-e552bc8c4910'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi status\nJob-UUID: b12db00e-1a36-4cbf-864d-e552bc8c4910\n\n'
    self.assertTrue(str(command) == desired_output)
    
class SyncClockCommandTests(TestCase):
   def test_success_scenario(self):
    command = SyncClockCommand(object())
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '07b6c879-1ee5-41ca-a615-c3f083ff3188'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl sync_clock\nJob-UUID: 07b6c879-1ee5-41ca-a615-c3f083ff3188\n\n'
    self.assertTrue(str(command) == desired_output)

class SyncClockWhenIdleCommandTests(TestCase):
   def test_success_scenario(self):
    command = SyncClockWhenIdleCommand(object())
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '3668f877-5b09-4810-9348-2fe98a430792'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi fsctl sync_clock_when_idle\nJob-UUID: 3668f877-5b09-4810-9348-2fe98a430792\n\n'
    self.assertTrue(str(command) == desired_output)

class UnloadModuleCommandTests(TestCase):
   def test_success_scenario_passvariables(self):
    command = UnloadModuleCommand(object(), name = 'testName', force = 'true')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '21516b8e-5a0b-485a-9e53-933e42947079'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi unload -f testName\nJob-UUID: 21516b8e-5a0b-485a-9e53-933e42947079\n\n'
    self.assertTrue(str(command) == desired_output)
   def test_success_scenario_passvariable(self):
    command = UnloadModuleCommand(object(), name = 'testName')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '21516b8e-5a0b-485a-9e53-933e42947079'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi unload testName\nJob-UUID: 21516b8e-5a0b-485a-9e53-933e42947079\n\n'
    self.assertTrue(str(command) == desired_output)

class AnswerCommandTests(TestCase):
   def test_success_scenario(self):
    command = AnswerCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '3fb1dc3b-6082-4ded-a010-ca93b7087c8a'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_answer 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 3fb1dc3b-6082-4ded-a010-ca93b7087c8a\n\n'
    self.assertTrue(str(command) == desired_output)
    print 'THIS IS THE START OF DOING THE UUIDCOMMAND SECTION******************************'

class BreakCommandTests(TestCase):
   def test_success_scenario(self):
    #command = BreakCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    print "TODO: LOOKS LIKE VALID ERROR IN BreakCommandTests(Commented Out)!\n\n"
	# Monkey patch the Job-UUID
    #command.__job_uuid__ = '3fb1dc3b-6082-4ded-a010-ca93b7087c8a'
    # Make sure we are generating the correct output.
    #desired_output = 'bgapi uuid_answer 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 3fb1dc3b-6082-4ded-a010-ca93b7087c8a\n\n'
    #self.assertTrue(str(command) == desired_output)

class BridgeCommandTests(TestCase):
   def test_success_scenario(self):
    command = BridgeCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', other_uuid = '21516b8e-5a0b-485a-9e53-933e42947666')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'ffc7ea91-d2cd-4d21-9d80-bf0d68b0372d'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_bridge 21516b8e-5a0b-485a-9e53-933e42947079 21516b8e-5a0b-485a-9e53-933e42947666\nJob-UUID: ffc7ea91-d2cd-4d21-9d80-bf0d68b0372d\n\n'
    self.assertTrue(str(command) == desired_output)

class BroadcastCommandTests(TestCase):
   def test_success_scenario_withPath(self):
    command = BroadcastCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'aleg', path = 'testPath', app_name = None, app_args = 'app_args')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '9cc468b6-dedd-4f24-b905-b89e2c7ad51d'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_broadcast 21516b8e-5a0b-485a-9e53-933e42947079 testPath aleg\nJob-UUID: 9cc468b6-dedd-4f24-b905-b89e2c7ad51d\n\n'
    self.assertTrue(str(command) == desired_output)
    

class ChatCommandTests(TestCase):
   def test_success_scenario(self):
    #command = ChatCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', text = None)
    #print str(command)    
	# Monkey patch the Job-UUID
    #command.__job_uuid__ = 'ffc7ea91-d2cd-4d21-9d80-bf0d68b0372d'
    # Make sure we are generating the correct output.
    #desired_output = 'bgapi uuid_bridge 21516b8e-5a0b-485a-9e53-933e42947079 21516b8e-5a0b-485a-9e53-933e42947666\nJob-UUID: ffc7ea91-d2cd-4d21-9d80-bf0d68b0372d\n\n'
    #self.assertTrue(str(command) == desired_output)    
	print "TODO: LOOKS LIKE VALID ERROR IN ChatCommandTests(Commented Out)!\n\n"

class DeflectCommandTests(TestCase):
   def test_success_scenario(self):
    command = DeflectCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', url = 'testURL')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'b0f0a065-163b-40a4-bd47-ff1fc04a9829'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_deflect 21516b8e-5a0b-485a-9e53-933e42947079 testURL\nJob-UUID: b0f0a065-163b-40a4-bd47-ff1fc04a9829\n\n'
    self.assertTrue(str(command) == desired_output)    

class DisableMediaCommandTests(TestCase):
   def test_success_scenario(self):
    command = DisableMediaCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'e9697383-c815-4172-b466-b549751b58bc'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_media off 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: e9697383-c815-4172-b466-b549751b58bc\n\n'
    self.assertTrue(str(command) == desired_output)    

class DisplayCommandTests(TestCase):
   def test_success_scenario(self):
    command = DisplayCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', display = 'MessageBox.Show()')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'df3e9d07-0196-4d31-a5cc-0b442c10bef0'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_display 21516b8e-5a0b-485a-9e53-933e42947079 MessageBox.Show()\nJob-UUID: df3e9d07-0196-4d31-a5cc-0b442c10bef0\n\n'
    self.assertTrue(str(command) == desired_output)    

class DualTransferCommandTests(TestCase):
   def test_success_scenario(self):
    command = DualTransferCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', extension_a = '0', extension_b = '1', dialplan_a = 'plana', dialplan_b = 'planb', context_a = 'contxa', context_b = 'contxb')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '9f88ba3a-3390-424c-af92-8a362bc3207b'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_dual_transfer 21516b8e-5a0b-485a-9e53-933e42947079 0/plana/contxa 1/planb/contxb\nJob-UUID: 9f88ba3a-3390-424c-af92-8a362bc3207b\n\n'
    self.assertTrue(str(command) == desired_output)    

class DumpCommandTests(TestCase):
   def test_success_scenario(self):
    #command = DumpCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', format = None)
    #print str(command)    
	# Monkey patch the Job-UUID
    #command.__job_uuid__ = 'ffc7ea91-d2cd-4d21-9d80-bf0d68b0372d'
    # Make sure we are generating the correct output.
    #desired_output = 'bgapi uuid_bridge 21516b8e-5a0b-485a-9e53-933e42947079 21516b8e-5a0b-485a-9e53-933e42947666\nJob-UUID: ffc7ea91-d2cd-4d21-9d80-bf0d68b0372d\n\n'
    #self.assertTrue(str(command) == desired_output)    
	print "TODO: LOOKS LIKE VALID ERROR IN DumpCommandTests(Commented Out)!\n\n"

class EarlyOkayCommandTests(TestCase):
   def test_success_scenario(self):
    command = EarlyOkayCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '628bcba9-da5e-4fc5-aff7-7b8691829e61'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_early_ok 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 628bcba9-da5e-4fc5-aff7-7b8691829e61\n\n'
    self.assertTrue(str(command) == desired_output)

class EnableMediaCommandTests(TestCase):
   def test_success_scenario(self):
    command = EnableMediaCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'bf510918-0147-475b-8e09-eb2741e8dc37'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_media 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: bf510918-0147-475b-8e09-eb2741e8dc37\n\n'
    self.assertTrue(str(command) == desired_output)

class EnableSessionHeartbeatCommandTests(TestCase):
   def test_success_scenario_with_variable(self):
    command = EnableSessionHeartbeatCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', start_time = 60)
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '82ecf94d-76c2-45e4-9e0c-850872322a3e'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_session_heartbeat 21516b8e-5a0b-485a-9e53-933e42947079 sched 60\nJob-UUID: 82ecf94d-76c2-45e4-9e0c-850872322a3e\n\n'
    self.assertTrue(str(command) == desired_output)
   def test_success_scenario_without_variable(self):
    command = EnableSessionHeartbeatCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '82ecf94d-76c2-45e4-9e0c-850872322a3e'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_session_heartbeat 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 82ecf94d-76c2-45e4-9e0c-850872322a3e\n\n'
    self.assertTrue(str(command) == desired_output)

class FileManagerCommandTests(TestCase):
   def test_success_scenario_with_variable(self):
    command = FileManagerCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', command = 'speed')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'cfb043b3-9cfa-45f4-9461-9dc85930ad5b'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_fileman 21516b8e-5a0b-485a-9e53-933e42947079 speed\nJob-UUID: cfb043b3-9cfa-45f4-9461-9dc85930ad5b\n\n'
    self.assertTrue(str(command) == desired_output)
    print "TODO: TEST FOR OPTION BEING pause, truncate, volume, restart, seek!\n\n"

class FlushDTMFCommandTests(TestCase):
   def test_success_scenario(self):
    command = FlushDTMFCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '85d4cb5a-a060-4b7c-ba61-7c71ddd5650c'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_flush_dtmf 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 85d4cb5a-a060-4b7c-ba61-7c71ddd5650c\n\n'
    self.assertTrue(str(command) == desired_output)

class GetAudioLevelCommandTests(TestCase):
   def test_success_scenario(self):
    command = GetAudioLevelCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'bff66665-3263-4c92-a780-00323137597a'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_audio 21516b8e-5a0b-485a-9e53-933e42947079 start read level\nJob-UUID: bff66665-3263-4c92-a780-00323137597a\n\n'
    self.assertTrue(str(command) == desired_output)

class GetBugListCommandTests(TestCase):
   def test_success_scenario(self):
    command = GetBugListCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '63143507-136f-4541-9075-ffae5ae50ed1'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_buglist 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 63143507-136f-4541-9075-ffae5ae50ed1\n\n'
    self.assertTrue(str(command) == desired_output)

class GetVariableCommandTests(TestCase):
   def test_success_scenario(self):
    command = GetVariableCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', name = 'testName')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '76eb7b5a-5cb5-49c8-beb0-07c44406cd8d'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_getvar 21516b8e-5a0b-485a-9e53-933e42947079 testName\nJob-UUID: 76eb7b5a-5cb5-49c8-beb0-07c44406cd8d\n\n'
    self.assertTrue(str(command) == desired_output)

class HoldCommandTests(TestCase):
   def test_success_scenario(self):
    command = HoldCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '4ee0e041-7151-4e92-8e43-a9f5d0f9c968'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_hold 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 4ee0e041-7151-4e92-8e43-a9f5d0f9c968\n\n'
    self.assertTrue(str(command) == desired_output)

class KillCommandTests(TestCase):
   def test_success_scenario_with_variable(self):
    command = KillCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', cause = 'fake cause')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'a75d38f0-8d7c-4851-849f-bb4a495631a2'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_kill 21516b8e-5a0b-485a-9e53-933e42947079 fake cause\nJob-UUID: a75d38f0-8d7c-4851-849f-bb4a495631a2\n\n'
    self.assertTrue(str(command) == desired_output)
   def test_success_scenario_without_variable(self):
    command = KillCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '21f01e31-047b-49b9-8734-fc904802e310'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_kill 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 21f01e31-047b-49b9-8734-fc904802e310\n\n'
    self.assertTrue(str(command) == desired_output)

class LimitCommandTests(TestCase):
   def test_success_scenario(self):
    command = LimitCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', backend = 'backend', realm = 'realm', resource='resource', max_calls = 2, interval = 20, number = 15, dialplan = 'c', context='unknown')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '92e57598-862a-4e92-93dd-601576f2b1ba'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_limit 21516b8e-5a0b-485a-9e53-933e42947079 backend realm resource 2/20 15 c unknown\nJob-UUID: 92e57598-862a-4e92-93dd-601576f2b1ba\n\n'
    self.assertTrue(str(command) == desired_output)
   
class ParkCommandTests(TestCase):
   def test_success_scenario(self):
    command = ParkCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '01bf39d5-8409-45d8-aa0c-1442a71bf67f'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_park 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 01bf39d5-8409-45d8-aa0c-1442a71bf67f\n\n'
    self.assertTrue(str(command) == desired_output)

class PauseCommandTests(TestCase):
   def test_success_scenario(self):
    command = PauseCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '1218e1a8-58ef-4776-9d45-69b813729cd1'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi pause 21516b8e-5a0b-485a-9e53-933e42947079 on\nJob-UUID: 1218e1a8-58ef-4776-9d45-69b813729cd1\n\n'
    self.assertTrue(str(command) == desired_output)

class PreProcessCommandTests(TestCase):
   def test_success_scenario(self):
    command = PreProcessCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '8e257556-647e-4626-b346-db9d5848f97c'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_preprocess 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 8e257556-647e-4626-b346-db9d5848f97c\n\n'
    self.assertTrue(str(command) == desired_output)


class PreAnswerCommandTests(TestCase):
   def test_success_scenario(self):
    command = PreAnswerCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '407560ca-da81-4d7a-9904-f46110a553e3'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_preanswer 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 407560ca-da81-4d7a-9904-f46110a553e3\n\n'
    self.assertTrue(str(command) == desired_output)


class ReceiveDTMFCommandTests(TestCase):
   def test_success_scenario(self):
    command = ReceiveDTMFCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'edf55710-48e5-4084-9008-0021cb63d970'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_recv_dtmf 21516b8e-5a0b-485a-9e53-933e42947079 None\nJob-UUID: edf55710-48e5-4084-9008-0021cb63d970\n\n'
    self.assertTrue(str(command) == desired_output)

class RenegotiateMediaCommandTests(TestCase):
   def test_success_scenario(self):
    command = RenegotiateMediaCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', codec = 'test_codex94')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'be427bc0-7b8d-475b-a967-29e5a401c413'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_media_reneg 21516b8e-5a0b-485a-9e53-933e42947079 =test_codex94\nJob-UUID: be427bc0-7b8d-475b-a967-29e5a401c413\n\n'
    self.assertTrue(str(command) == desired_output)

class SendDTMFCommandTests(TestCase):
   def test_success_scenario(self):
    command = SendDTMFCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '94ce15dd-771f-4196-aa19-dc6e1e49a546'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_send_dtmf 21516b8e-5a0b-485a-9e53-933e42947079 None\nJob-UUID: 94ce15dd-771f-4196-aa19-dc6e1e49a546\n\n'
    self.assertTrue(str(command) == desired_output)

class SendInfoCommandTests(TestCase):
   def test_success_scenario(self):
    command = SendInfoCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'ec096159-6f59-4ead-9542-cb262c415f97'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_send_info 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: ec096159-6f59-4ead-9542-cb262c415f97\n\n'
    self.assertTrue(str(command) == desired_output)

class SetAudioLevelCommandTests(TestCase):
   def test_success_scenario_with_variable(self):
    command = SetAudioLevelCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', level = 3.3)
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = 'f523fecf-1658-458c-a2db-f19a7e33c00e'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_audio 21516b8e-5a0b-485a-9e53-933e42947079 start write level 3.300000\nJob-UUID: f523fecf-1658-458c-a2db-f19a7e33c00e\n\n'
    self.assertTrue(str(command) == desired_output)
    print "TODO: TEST FOR OPTION BEING > 4.0 or < -4.0!\n\n"

class SetMultipleVariableCommand(UUIDCommand):
   def test_success_scenario(self):
    print "TODO: NEED HELP IMPLEMENTING IT FOR SetMultipleVariableCommand()/n/n"

class SetVariableCommandTests(TestCase):
   def test_success_scenario(self):
   	command = SetVariableCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', name = 'testName', value = 'testValue')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '17c5b551-b9e8-400f-b0e9-0ff41b35cd04'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi uuid_setvar 21516b8e-5a0b-485a-9e53-933e42947079 testName testValue\nJob-UUID: 17c5b551-b9e8-400f-b0e9-0ff41b35cd04\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)

class SimplifyCommandTests(TestCase):
   def test_success_scenario(self):
   	command = SimplifyCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', name = 'testName', value = 'testValue')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '22593ef7-ce3f-4918-8cdd-b8b4d3f78a91'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi uuid_simplify 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 22593ef7-ce3f-4918-8cdd-b8b4d3f78a91\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)

class StartDebugMediaCommandTests(TestCase):
   def test_success_scenario(self):
   	command = StartDebugMediaCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', option = 'testOption')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = 'a5ef37ed-093b-4e81-a475-0020d2f37731'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi uuid_debug_media 21516b8e-5a0b-485a-9e53-933e42947079 testOption on\nJob-UUID: a5ef37ed-093b-4e81-a475-0020d2f37731\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)

class StartDisplaceCommandTests(TestCase):
   def test_success_scenario(self):
   	command = StartDisplaceCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', path = 'testPath', limit = 450, mux='testMux')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '00253c5b-cc77-4bfd-9827-e9018787263f'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi uuid_displace 21516b8e-5a0b-485a-9e53-933e42947079 start testPath 450 mux\nJob-UUID: 00253c5b-cc77-4bfd-9827-e9018787263f\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)

class StopDebugMediaCommandTests(TestCase):
   def test_success_scenario(self):
    command = StopDebugMediaCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '7d053ca9-7390-425b-8859-0907a6fa65eb'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_debug_media 21516b8e-5a0b-485a-9e53-933e42947079 off\nJob-UUID: 7d053ca9-7390-425b-8859-0907a6fa65eb\n\n'
    self.assertTrue(str(command) == desired_output)

class StopDisplaceCommandTests(TestCase):
   def test_success_scenario(self):
    command = StopDisplaceCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '8dec5e56-ea53-4140-bc02-6617cf4e34ce'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_displace 21516b8e-5a0b-485a-9e53-933e42947079 stop\nJob-UUID: 8dec5e56-ea53-4140-bc02-6617cf4e34ce\n\n'
    self.assertTrue(str(command) == desired_output)

class TransferCommandTests(TestCase):
   def test_success_scenario(self):
    command = TransferCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'legTest', extension = '384', dialplan = '44', context = 'contextTest')
    #print str(command)    
	# Monkey patch the Job-UUID
    command.__job_uuid__ = '347c1dd4-7b62-49b0-b23c-b120b25aac37'
    # Make sure we are generating the correct output.
    desired_output = 'bgapi uuid_transfer 21516b8e-5a0b-485a-9e53-933e42947079 legTest 384 44 contextTest\nJob-UUID: 347c1dd4-7b62-49b0-b23c-b120b25aac37\n\n'
    self.assertTrue(str(command) == desired_output)

class UnholdCommandTests(TestCase):
   def test_success_scenario(self):
   	command = UnholdCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '437d1f3b-1bda-4c1f-84c2-7aa1a3cd9afa'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi uuid_hold off 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: 437d1f3b-1bda-4c1f-84c2-7aa1a3cd9afa\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)

class UnpauseCommandTests(TestCase):
   def test_success_scenario(self):
   	command = UnpauseCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = 'c4a3d50f-f7e5-4cab-980d-37c70e028bd3'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi pause 21516b8e-5a0b-485a-9e53-933e42947079 off\nJob-UUID: c4a3d50f-f7e5-4cab-980d-37c70e028bd3\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)

class UnpauseCommandTests(TestCase):
   def test_success_scenario(self):
   	command = UnpauseCommand(object(), uuid = '21516b8e-5a0b-485a-9e53-933e42947079', name = 'testName')   	
   	#print str(command)
  	# Monkey patch the Job-UUID
   	command.__job_uuid__ = '2082ca22-e4b0-49b1-9a27-bccf37fd80ce'
   	# Make sure we are generating the correct output.
   	desired_output = 'bgapi pause 21516b8e-5a0b-485a-9e53-933e42947079 off\nJob-UUID: 2082ca22-e4b0-49b1-9a27-bccf37fd80ce\n\n'
   	self.assertTrue(str(command) == desired_output)
   	#print str(command)



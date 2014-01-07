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
    print str(command)
    print desired_output
    self.assertTrue(str(command) == desired_output)
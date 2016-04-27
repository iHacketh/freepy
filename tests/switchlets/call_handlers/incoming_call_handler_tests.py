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
# Nishad Musthafa  <nishadmusthafa@gmail.com>

from lib.commands import AnswerCommand, KillCommand
from lib.core import InitializeSwitchletEvent
from lib.esl import Event
from lib.server import RegisterJobObserverCommand, UnregisterJobObserverCommand
from switchlets.call_handlers import IncomingCallHandler
from switchlets.call_utilities import ActionExecutor, ExecutionComplete, StartExecution
from switchlets.data_connector import QueryContext, QueryResult
from unittest import TestCase
import mock, time

class IncomingCallHandlerTests(TestCase):
  def test_incoming_call_handler_flow_success(self):
    incoming_call_handler = IncomingCallHandler.start()
    
    with mock.patch('switchlets.data_connector.data_connector.DataConnector.on_receive') as mock_data_connector_on_receive:
      with mock.patch('switchlets.call_utilities.ActionExecutor.on_receive') as mock_action_executor_on_receive:
        initialize_switchlet = mock.Mock(spec=InitializeSwitchletEvent)
        dispatcher = mock.Mock()
        initialize_switchlet.get_dispatcher = mock.Mock(return_value=dispatcher)
        
        # State 'not ready' to 'waiting for incoming call'
        incoming_call_handler.tell({'content': initialize_switchlet})
        time.sleep(2)

        channel_create_headers = {
                                'Content-Type':'text/event-plain',
                                'Event-Name': 'CHANNEL_CREATE',
                                'Caller-Direction': 'inbound',
                                'Channel-Call-UUID': 'fake_call_uuid',
                                'Caller-Destination-Number': 'sample_to_number'}
        channel_create = Event(channel_create_headers)

        # State 'waiting for incoming call' to 'call started. fetching app'
        incoming_call_handler.tell({'content': channel_create})
        time.sleep(2)
        
        self.assertEquals(mock_data_connector_on_receive.call_count, 1)
        passed_query = mock_data_connector_on_receive.call_args_list[0][0][0]['content']
        self.assertTrue(isinstance(passed_query, QueryContext))
        self.assertEquals(passed_query.get_sender().actor_urn, incoming_call_handler.actor_urn)
        self.assertEquals(passed_query.get_model(), 'number_mappings')
        self.assertEquals(passed_query.get_key(), 'sample_to_number')
        self.assertEquals(passed_query.get_failure_destination_state(), 'failed query. stopping call')
        self.assertEquals(passed_query.get_success_destination_state(), 'fetching execution logic')

        query_result = QueryResult('sample_app_name', 'sample message', 'fetching execution logic')

        # State 'call started. fetching app' to 'fetching execution logic'
        incoming_call_handler.tell({'content': query_result})
        time.sleep(2)

        self.assertEquals(mock_data_connector_on_receive.call_count, 2)
        passed_query = mock_data_connector_on_receive.call_args_list[1][0][0]['content']
        self.assertTrue(isinstance(passed_query, QueryContext))
        self.assertEquals(passed_query.get_sender().actor_urn, incoming_call_handler.actor_urn)
        self.assertEquals(passed_query.get_model(), 'app_data')
        self.assertEquals(passed_query.get_key(), 'sample_app_name')
        self.assertEquals(passed_query.get_failure_destination_state(), 'failed query. stopping call')
        self.assertEquals(passed_query.get_success_destination_state(), 'got logic. answering call')

        query_result = QueryResult(['sample_action_list'], 'sample message', 'got logic. answering call')

        # State 'fetching execution logic' to 'got logic. answering call'
        incoming_call_handler.tell({'content': query_result})
        time.sleep(2)

        self.assertEquals(dispatcher.mock_calls[0].call_list()[0][0], 'tell')
        self.assertEquals(dispatcher.mock_calls[1].call_list()[0][0], 'tell')
        first_message_sent_to_dispatcher = dispatcher.mock_calls[0].call_list()[0][1][0]['content']
        second_message_sent_to_dispatcher = dispatcher.mock_calls[1].call_list()[0][1][0]['content']
        self.assertTrue(isinstance(first_message_sent_to_dispatcher, RegisterJobObserverCommand))
        self.assertEquals(first_message_sent_to_dispatcher.get_observer().actor_urn, incoming_call_handler.actor_urn)
        expected_command = 'bgapi uuid_answer fake_call_uuid\nJob-UUID: %s\n\n' % first_message_sent_to_dispatcher.get_job_uuid()
        self.assertEquals(str(second_message_sent_to_dispatcher), expected_command)
        self.assertTrue(isinstance(second_message_sent_to_dispatcher, AnswerCommand))

        call_answer_headers = {
                                'Content-Type':'text/event-plain',
                                'Event-Name': 'BACKGROUND_JOB',
                                'Job-Command-Arg': 'fake_call_uuid',
                                'Job-Command': 'uuid_answer'
                                }
        call_answer = Event(call_answer_headers)

        # State 'got logic. answering call' to 'executing call logic'
        incoming_call_handler.tell({'content': call_answer})
        time.sleep(2)

        self.assertEquals(mock_action_executor_on_receive.call_count, 1)
        execution_context = mock_action_executor_on_receive.call_args_list[0][0][0]['content']

        self.assertTrue(isinstance(execution_context, StartExecution))
        self.assertEquals(execution_context.get_context(), ['sample_action_list'])
        self.assertEquals(execution_context.get_call_uuid(), 'fake_call_uuid')
        self.assertEquals(execution_context.get_dispatcher(), dispatcher)
        self.assertEquals(execution_context.get_sender().actor_urn, incoming_call_handler.actor_urn)
        self.assertEquals(dispatcher.mock_calls[2].call_list()[0][0], 'tell')
        message_sent_to_dispatcher = dispatcher.mock_calls[2].call_list()[0][1][0]['content']
        self.assertTrue(isinstance(message_sent_to_dispatcher, UnregisterJobObserverCommand))

        execution_complete = ExecutionComplete()

        # State 'executing call logic' to 'terminate call'
        incoming_call_handler.tell({'content': execution_complete})
        time.sleep(2)

        self.assertEquals(dispatcher.mock_calls[3].call_list()[0][0], 'tell')
        self.assertEquals(dispatcher.mock_calls[4].call_list()[0][0], 'tell')
        first_message_sent_to_dispatcher = dispatcher.mock_calls[3].call_list()[0][1][0]['content']
        second_message_sent_to_dispatcher = dispatcher.mock_calls[4].call_list()[0][1][0]['content']
        self.assertTrue(isinstance(first_message_sent_to_dispatcher, RegisterJobObserverCommand))
        self.assertEquals(first_message_sent_to_dispatcher.get_observer().actor_urn, incoming_call_handler.actor_urn)
        expected_command = 'bgapi uuid_kill fake_call_uuid\nJob-UUID: %s\n\n' % first_message_sent_to_dispatcher.get_job_uuid()
        self.assertEquals(str(second_message_sent_to_dispatcher), expected_command)
        self.assertTrue(isinstance(second_message_sent_to_dispatcher, KillCommand))

        call_terminate_headers = {
                                'Content-Type':'text/event-plain',
                                'Event-Name': 'BACKGROUND_JOB',
                                'Job-Command-Arg': 'fake_call_uuid',
                                'Job-Command': 'uuid_kill'
                                }
        call_terminate = Event(call_terminate_headers)

        # State 'executing call logic' to 'call terminated'
        incoming_call_handler.tell({'content': call_terminate})
        time.sleep(2)

        self.assertEquals(dispatcher.mock_calls[5].call_list()[0][0], 'tell')
        message_sent_to_dispatcher = dispatcher.mock_calls[5].call_list()[0][1][0]['content']
        self.assertTrue(isinstance(message_sent_to_dispatcher, UnregisterJobObserverCommand))
        self.assertEquals(incoming_call_handler._actor.__state__, 'call terminated')

    incoming_call_handler.stop()

  def test_incoming_call_handler_flow_query_error(self):
    incoming_call_handler = IncomingCallHandler.start()
    
    with mock.patch('switchlets.data_connector.data_connector.DataConnector.on_receive') as mock_data_connector_on_receive:
      with mock.patch('switchlets.call_utilities.ActionExecutor.on_receive') as mock_action_executor_on_receive:
        initialize_switchlet = mock.Mock(spec=InitializeSwitchletEvent)
        dispatcher = mock.Mock()
        initialize_switchlet.get_dispatcher = mock.Mock(return_value=dispatcher)

        # State 'not ready' to 'waiting for incoming call'
        incoming_call_handler.tell({'content': initialize_switchlet})
        time.sleep(2)

        channel_create_headers = {
                                'Content-Type':'text/event-plain',
                                'Event-Name': 'CHANNEL_CREATE',
                                'Caller-Direction': 'inbound',
                                'Channel-Call-UUID': 'fake_call_uuid',
                                'Caller-Destination-Number': 'sample_to_number'}

        channel_create = Event(channel_create_headers)

        # State 'waiting for incoming call' to 'call started. fetching app'
        incoming_call_handler.tell({'content': channel_create})
        time.sleep(2)
        
        self.assertEquals(mock_data_connector_on_receive.call_count, 1)
        passed_query = mock_data_connector_on_receive.call_args_list[0][0][0]['content']
        self.assertTrue(isinstance(passed_query, QueryContext))
        self.assertEquals(passed_query.get_sender().actor_urn, incoming_call_handler.actor_urn)
        self.assertEquals(passed_query.get_model(), 'number_mappings')
        self.assertEquals(passed_query.get_key(), 'sample_to_number')
        self.assertEquals(passed_query.get_failure_destination_state(), 'failed query. stopping call')
        self.assertEquals(passed_query.get_success_destination_state(), 'fetching execution logic')

        query_result = QueryResult('sample_app_name', 'sample message', 'failed query. stopping call')

        # State 'call started. fetching app' to 'failed query. stopping call'
        # State 'failed query. stopping call' to 'terminate call'
        incoming_call_handler.tell({'content': query_result})
        time.sleep(2)

        self.assertEquals(dispatcher.mock_calls[0].call_list()[0][0], 'tell')
        self.assertEquals(dispatcher.mock_calls[1].call_list()[0][0], 'tell')
        first_message_sent_to_dispatcher = dispatcher.mock_calls[0].call_list()[0][1][0]['content']
        second_message_sent_to_dispatcher = dispatcher.mock_calls[1].call_list()[0][1][0]['content']
        self.assertTrue(isinstance(first_message_sent_to_dispatcher, RegisterJobObserverCommand))
        self.assertEquals(first_message_sent_to_dispatcher.get_observer().actor_urn, incoming_call_handler.actor_urn)
        expected_command = 'bgapi uuid_kill fake_call_uuid\nJob-UUID: %s\n\n' % first_message_sent_to_dispatcher.get_job_uuid()
        self.assertEquals(str(second_message_sent_to_dispatcher), expected_command)
        self.assertTrue(isinstance(second_message_sent_to_dispatcher, KillCommand))

        call_terminate_headers = {
                                'Content-Type':'text/event-plain',
                                'Event-Name': 'BACKGROUND_JOB',
                                'Job-Command-Arg': 'fake_call_uuid',
                                'Job-Command': 'uuid_kill'
                                }
        call_terminate = Event(call_terminate_headers)

        # State 'terminate call' to 'call terminated'
        incoming_call_handler.tell({'content': call_terminate})
        time.sleep(2)

        self.assertEquals(dispatcher.mock_calls[2].call_list()[0][0], 'tell')
        message_sent_to_dispatcher = dispatcher.mock_calls[2].call_list()[0][1][0]['content']
        self.assertTrue(isinstance(message_sent_to_dispatcher, UnregisterJobObserverCommand))
        self.assertEquals(incoming_call_handler._actor.__state__, 'call terminated')

    incoming_call_handler.stop()
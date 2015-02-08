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

from lib.core import Switchlet
from lib.fsm import Action, FiniteStateMachine
from data_set import app_data, ivr_info, number_mappings

import logging

class DataStoreContext(object):
  def __init__(self, caller_ref, context):
    self.__caller_ref__ = caller_ref
    self.__context__ = context

  def get_caller_ref(self):
    return self.__caller_ref__

  def get_context(self):
    return self.__context__

class CallExecution(object):
  def __init__(self, task_list):
    self.__task_list__ = task_list

class QueryError(object):
  pass

class QuerySuccess(object):
  def __init__(self, query_result):
    self.__query_result__ = query_result

  def get_query_result(self):
    return self.__query_result__

class DataConnector(FiniteStateMachine, Switchlet):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'connected'),
    ('connected', 'querying'),
    ('querying', 'connected'),
  ]
  
  def __init__(self, *args, **kwargs):
    super(DataConnector, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('call_handlers.data_connector')
    self.connect_to_data_store()
    

  def connect_to_data_store(self):
    # This can be a configurable datastore, In an ideal situation, this should
    # be an in memory cache that is a replica of the main db. The in memory store
    # should reside on the same machine as freepy to do away with network delays. 
    # For the purposes of this prototype, I'm using a dictionary in a python file.
    
    # Right now, I'm not adding any async code here. Ideally, there would be another actor to 
    # connect to the db and a tell would be made to that actor to connect to the db. 
    self.__app_data__ = app_data
    self.__number_mappings__ = number_mappings
    # the db connection actor would then tell this Actor to shift to "connected" state
    self.transition(to = 'connected')

  @Action(state = 'querying')
  def query_data_store(self, message):
    caller_ref = message.get_caller_ref()
    context = message.get_context()
    try:
      to_number = context.get('to')
      app = self.__number_mappings__.get(to_number)
      tasks = self.__app_data__.get(app)
    except KeyError:
      self.__logger__.error('App improperly configured for to number %s' % to_number)
      query_error = QueryError()
      caller_ref.tell({'content': query_error})
      return
    query_success = QuerySuccess(tasks)
    caller_ref.tell({ 'content': query_success})

  def on_receive(self, message):
    message = message.get('content')
    if isinstance(message, DataStoreContext):
      self.transition(to = 'querying', event = message)

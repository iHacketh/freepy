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

class QueryContext(object):
  def __init__(self, **kwargs):
    self.__logger__ = logging.getLogger('call_handlers.data_connector.QueryContext')
    try:
      self.__caller_ref__ = kwargs['caller_ref']
      self.__model__ = kwargs['model']
      self.__key__ = kwargs['key']
      self.__failure_destination_state__ = kwargs['failure_destination_state']
      self.__success_destination_state__ = kwargs['success_destination_state']
    except KeyError, e:
      self.__logger__.error('Query Context initialized without mandatory parameter %s' % e)
      raise e

  def get_caller_ref(self):
    return self.__caller_ref__

  def get_model(self):
    return self.__model__

  def get_key(self):
    return self.__key__

  def get_failure_destination_state(self):
      return self.__failure_destination_state__

  def get_success_destination_state(self):
      return self.__success_destination_state__

class QueryResult(object):
  def __init__(self, query_result, message, destination_state):
    self.__query_result__ = query_result
    self.__message__ = message
    self.__destination_state__ = destination_state

  def get_query_result(self):
    return self.__query_result__

  def get_message(self):
    return self.__message__

  def get_destination_state(self):
    return self.__destination_state__

class QueryDone(object):
  pass

class DataConnector(FiniteStateMachine, Switchlet):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'connected'),
    ('connected', 'querying'),
    ('querying', 'connected'),
  ]
  
  def __init__(self, *args, **kwargs):
    super(DataConnector, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('call_handlers.data_connector.DataConnector')
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
  def run_query(self, message):
    caller_ref = message.get_caller_ref()
    model = message.get_model()
    key = message.get_key()
    try:
      # This may look really hacky. But it makes much more sense to design code this
      # way if you want to query data from a real datastore in the future as opposed to 
      # how it is being done now from a python variable
      query = model + '.get("' + key + '")\n'
      result = eval(query)
      result_message = 'Query Successful for key %s in model %s' % (key, model)
      destination_state = message.get_success_destination_state()
    except KeyError:
      result_message = 'Query failed. No key %s in model %s' % (key, model)
      result = None
      destination_state = message.get_failure_destination_state()
      self.__logger__.error(message)

    query_result = QueryResult(result, result_message, destination_state)
    caller_ref.tell({ 'content': query_result})
    query_done = QueryDone()
    self.actor_ref.tell({ 'content': query_done})

  def on_receive(self, message):
    message = message.get('content')
    if isinstance(message, QueryContext):
      self.transition(to = 'querying', event = message)
    if isinstance(message, QueryContext):
      self.transition(to = 'connected')

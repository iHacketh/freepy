from lib.commands import *
from lib.events import *
from lib.server import *
from pykka import ThreadingActor

import logging
import urllib

class Monitor(ThreadingActor):
  def __init__(self, *args, **kwargs):
    super(Monitor, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('heartbeat.monitor')
    self.__dispatcher__ = None


  def on_receive(self, message):
    # Necessary because all pykka messages must be dicts.
    message = message.get('content')
    if isinstance(message, InitializeSwitchletEvent):
      # If we are being initialized store a reference to the dispatcher.
      self.__dispatcher__ = message.get_dispatcher()
    elif isinstance(message, Event):
      content_type = message.get_header('Content-Type')
      # Handle the response for StatusCommand.
      if content_type == 'command/reply':
        uuid = message.get_header('Job-UUID')
        command = RegisterJobObserverEvent(self.actor_ref, uuid)
        self.__dispatcher__.tell({'content': command})
        self.__logger__.info('Registered to receive events with Job-UUID: %s' % uuid)
      elif content_type == 'text/event-plain':
        name = message.get_header('Event-Name')
        # Handle a heartbeat event.
        if name == 'HEARTBEAT':
          # Ask FreeSWITCH for a status.
          command = StatusCommand(self.actor_ref)
          self.__dispatcher__.tell({'content': command})
        # Handle a background job event (Status).
        elif name == 'BACKGROUND_JOB':
          self.__logger__.info(message.get_body())
          uuid = message.get_header('Job-UUID')
          command = UnregisterJobObserverEvent(uuid)
          self.__dispatcher__.tell({'content': command})
          self.__logger__.info('Unregistered to receive events with Job-UUID: %s' % uuid)

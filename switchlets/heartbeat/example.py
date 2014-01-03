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
    # If we are being initialized store the reference to the dispatcher.
    if isinstance(message, InitializeSwitchletEvent):
      self.__dispatcher__ = message.get_dispatcher()
    else:
      # Handle the message.
      self.__logger__.info('%s', self)
      header = message.get_header('Up-Time')
      uptime = urllib.unquote(header)
      self.__logger__.info('The system has been up for %s', uptime)
      # Send a status command.
      command = StatusCommand(self)
      self.__dispatcher__.tell({'content': command})

from pykka import ThreadingActor

import logging
import urllib

class Monitor(ThreadingActor):
  def __init__(self, *args, **kwargs):
    super(Monitor, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('heartbeat.monitor')

  def on_receive(self, message):
    # Necessary because all pykka messages must be dicts.
    message = message.get('content')
    # Handle the message.
    header = message.get_header('Up-Time')
    uptime = urllib.unquote(header)
    self.__logger__.info('The system has been up for %s', uptime)
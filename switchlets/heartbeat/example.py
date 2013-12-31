from pykka import ThreadingActor

import logging

class Monitor(ThreadingActor):
  def __init__(self, *args, **kwargs):
    super(Monitor, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('heartbeat.monitor')

  def on_receive(self, message):
    self.__logger__.info('The system has been up for %s', message.get_header('Up-Time'))
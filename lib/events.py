class InitializeSwitchletEvent(object):
  def __init__(self, dispatcher):
    self.__dispatcher__ = dispatcher

  def get_dispatcher(self):
    return self.__dispatcher__
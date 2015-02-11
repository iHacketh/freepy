from lib.core import InitializeSwitchletEvent, Switchlet
from lib.esl import Event
from lib.fsm import Action, FiniteStateMachine
from lib.server import WatchEventCommand, UnwatchEventCommand
import logging
from utils import ExecutionComplete, SendMessageCommand, StartExecution

class PlayCommand(SendMessageCommand):
  def __init__(self, *args, **kwargs):
    self.__app_name__ = 'playback'
    self.__path__ = kwargs.get('path')
    super(PlayCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    # For now, I'm using a tone. Will customize this to 
    # add more functionality like remote http urls later
    # remote http urls will also need an external mechanism
    # to cache the mp3's locally so that time isn't wasted
    # on fetching over the network every time. 
    arg = self.__path__
    arglen = len(arg)
    arguments = 'content-type: text/plain\ncontent-length: %d\n\n%s\n' % (arglen, arg)
    return super(PlayCommand, self).__str__() + arguments

class Play(FiniteStateMachine, Switchlet):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'ready'),
    ('ready', 'sending play command'),
    ('sending play command', 'complete'),
  ]

  def __init__(self, *args, **kwargs):
    super(Play, self).__init__(*args, **kwargs)
    self.__dispatcher__ = None
    self.__sender__ = None
    self.__call_uuid__ = None
    self.__logger__ = logging.getLogger('switchlets.call_utilities.play.Play')
    self.transition(to = 'ready')

  def get_call_uuid(self):
    return self.__call_uuid__

  def configure(self, message):
    self.__dispatcher__ = message.get_dispatcher()
    self.__playback_path__ = message.get_context()
    self.__sender__ = message.get_sender()
    self.__call_uuid__ = message.get_call_uuid()

  @Action(state = 'sending play command')
  def send_play_command(self, message):
    play_command = PlayCommand(self.__sender__, self.__call_uuid__, path = self.__playback_path__)
    watch_command = WatchEventCommand(self.actor_ref, name="Event-Name", value="PLAYBACK_STOP")
    self.__dispatcher__.tell({'content': watch_command})
    self.__dispatcher__.tell({'content': play_command})

  @Action(state = 'complete')
  def stop_play(self, message):
    execution_complete = ExecutionComplete()
    self.__sender__.tell({'content': execution_complete})

  def on_receive(self, message):
    message = message.get('content')
    if isinstance(message, StartExecution):
      self.configure(message)
      self.transition(to = 'sending play command', event = message)
    elif isinstance(message, Event):
      content_type = message.get_header('Content-Type')

      if content_type == 'text/event-plain':
        name = message.get_header('Event-Name')
        call_uuid = message.get_header('Channel-Call-UUID')
        if name == 'PLAYBACK_STOP' and call_uuid == self.get_call_uuid():
          unwatch_command = UnwatchEventCommand(name="Event-Name", value="PLAYBACK_STOP")
          self.__dispatcher__.tell({'content': unwatch_command})
          self.transition(to = 'complete')

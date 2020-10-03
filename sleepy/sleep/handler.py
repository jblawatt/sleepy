

from enum import Enum

from sleepy.sleep.thread import SleepThread
from sleepy.utils import EndlessIterator
from sleepy.sleep.thread import SleepEvents
from sleepy.player import player_factory
from sleepy import config

from typing import Callable


class SleepActions(Enum):
    PLAY = 0
    NEXT = 1
    STOP = 2


class SleepHandler:

    _sleep_thread: SleepThread = None
    _sleep_actions: EndlessIterator = None
    _sleep_event_handler: list = []

    def __init__(self):
        self._init_actions()

    def _get_config_intervals(self):
        """
        :returns: List of intervals from config or inital
        """
        c = config.get()
        fallback = '10,20,30,40'
        intervals_str = c.get('sleep', 'steps', fallback=fallback)
        return map(int, map(str.strip, intervals_str.split(',')))

    def _init_actions(self):
        """
        Initializes actions from config file.
        """
        intervals = self._get_config_intervals()
        self._sleep_actions = EndlessIterator(
            (SleepActions.PLAY, next(intervals)),
            *((SleepActions.NEXT, i) for i in intervals),
            (SleepActions.STOP, None),
        )

    def connect_event(self, event: SleepEvents, callback: Callable):
        self._sleep_event_handler.append((event, callback))

    def sleep_timedelta(self):
        if self._sleep_thread:
            return self._sleep_thread.sleep_timedelta()
        return None

    def iter_sleep(self):
        if self._sleep_thread is not None and \
                self._sleep_thread.is_destroyed():
            # wenn der Time schonmal abgelaufen war
            # dann starten wir ihn neu
            self._sleep_thread = None
            self._init_actions()

        action, minutes = next(self._sleep_actions)

        if action == SleepActions.PLAY:
            player_name = config.get().get('sleep', 'player')
            player = player_factory(player_name)
            self._sleep_thread = SleepThread(player)
            self._sleep_thread.set_callbacks(self._sleep_event_handler)
            # FIXME. Mussd assein oder geht das über den __init__?
            self._sleep_thread.daemon = True
            self._sleep_thread.start()
            self._sleep_thread.activate(minutes)

        if action == SleepActions.NEXT:
            self._sleep_thread.activate(minutes)

        if action == SleepActions.STOP:
            self._sleep_thread.destroy()
            self._sleep_thread = None

    def next_message(self):
        next_action, minutes = self._sleep_actions.next()
        if next_action == SleepActions.PLAY:
            return 'play'
        if next_action == SleepActions.NEXT:
            return '+ %s' % minutes
        if next_action == SleepActions.STOP:
            return 'stop'

    def is_active(self):
        if self._sleep_thread is None:
            return False
        return self._sleep_thread.is_active()

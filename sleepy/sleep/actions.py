
from sleepy.sleep.thread import SleepThread
from sleepy.player import VLCPlayer
from abc import ABCMeta, abstractmethod


class SleepAction:

    __meta__ = ABCMeta

    @abstractmethod
    def apply(self, sleep_thread):
        pass

    @abstractmethod
    def get_text(self):
        pass


class StartSleepAction(SleepAction):

    _start_minutes: int = 0

    def __init__(self, start_minutes: int):
        self._start_minutes = start_minutes

    def apply(self, sleep_thread: SleepThread) -> None:
        if sleep_thread is None:
            # TODO: Konfiguration muss woanders her kommen
            sleep_thread = SleepThread(VLCPlayer())
        sleep_thread.activate(self._start_minutes)

    def get_text(self) -> str:
        return 'start'


class StopSleepAction(SleepAction):

    def apply(self, sleep_thread: SleepThread) -> None:
        # TODO: So kann das nicht klappen.
        sleep_thread.deactivate()
        sleep_thread = None

    def get_text(self) -> str:
        return 'stop'


class SetTimeSleepAction(StartSleepAction):

    def get_text(self) -> str:
        return 'set %s' % self._start_minutes


from threading import Thread
from time import sleep
from datetime import datetime, timedelta
from enum import Enum
from sleepy.player import PlayerBase


class SleepEvents(Enum):
    DESTROYED = 1
    ACTIVATED = 2
    STOPPED = 3
    STARTED = 4


class ModesEnum(Enum):
    ACTIVE = 0
    INACTIVE = 1
    DESTROYED = 2
    GONE_TO_SLEEP = 3


class SleepThread(Thread):

    _sleep_at: datetime = None
    _mode: ModesEnum = None
    _player: PlayerBase = None

    def __init__(self, player, daemon=True):
        super().__init__(daemon=daemon)
        self._player = player

    def _is_active(self):
        return self._mode == ModesEnum.ACTIVE

    is_active = _is_active

    def _is_destoryed(self):
        return self._mode == ModesEnum.DESTROYED

    is_destroyed = _is_destoryed

    def _call_event(self, event: SleepEvents, *args, **kwargs):
        for etype, callback in self._callbacks:
            if etype == event:
                callback(*args, **kwargs)

    def _call_stop_event(self):
        self._call_event(SleepEvents.STOPPED)

    def _call_destroyed_event(self):
        self._call_event(SleepEvents.DESTROYED)

    def _call_activate_event(self, minutes):
        self._call_event(SleepEvents.ACTIVATED, minutes=minutes)

    def run(self):
        while True:
            if self._is_destoryed():
                break
            sleep(0.5)
            if not self._is_active():
                continue
            print('%s sec until stop' %
                  (self._sleep_at - datetime.now()).seconds)
            if self._sleep_at < datetime.now():
                self._goto_sleep()

    def sleep_timedelta(self):
        return self._sleep_at - datetime.now()

    def activate(self, minutes: int):
        # FIXME: wieder auf minuten umstellen
        self._sleep_at = datetime.now() + timedelta(seconds=minutes)
        self._mode = ModesEnum.ACTIVE
        self._player.play()
        print('activate %s min until shutdown' % minutes)
        self._call_activate_event(minutes=minutes)

    def deactivate(self):
        self._sleep_at = None
        self._mode = ModesEnum.INACTIVE
        self._player.stop()
        print('deactivate')
        self._call_stop_event()

    def destroy(self):
        self._sleep_at = None
        if self._player is not None:
            self._player.stop()
            self._player = None
        self._mode = ModesEnum.DESTROYED
        self._call_destroyed_event()

    def _goto_sleep(self):
        self.destroy()

    def set_callbacks(self, cb):
        self._callbacks = cb

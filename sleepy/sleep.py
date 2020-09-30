
from threading import Thread
from time import sleep
from datetime import datetime, timedelta
from enum import Enum
from player import PlayerBase


class ModesEnum(Enum):
    ACTIVE = 0
    INACTIVE = 1
    DESTROYED = 2
    GONE_TO_SLEEP = 3


class SleepThread(Thread):

    _sleep_at: datetime = None
    _mode: ModesEnum = None
    _player: PlayerBase = None

    def __init__(self, player):
        super().__init__()
        self._player = player

    def _is_active(self):
        return self._mode == ModesEnum.ACTIVE

    def _is_destoryed(self):
        return self._mode == ModesEnum.DESTROYED

    is_destroyed = _is_destoryed

    def run(self):
        while True:
            if self._is_destoryed():
                break
            sleep(0.5)
            if not self._is_active():
                continue
            print('%s sec until stop' % (self._sleep_at - datetime.now()).seconds)
            if self._sleep_at < datetime.now():
                self._goto_sleep()

    def activate(self, minutes: int):
        # FIXME: wieder auf minuten umstellen
        self._sleep_at = datetime.now() + timedelta(seconds=minutes)
        self._mode = ModesEnum.ACTIVE
        self._player.play()
        print('activate %s min until shutdown' % minutes)

    def deactivate(self):
        self._sleep_at = None
        self._mode = ModesEnum.INACTIVE
        self._player.stop()
        print('deactivate')

    def destroy(self):
        self._sleep_at = None
        if self._player is not None:
            self._player.stop()
            self._player = None
        self._mode = ModesEnum.DESTROYED

    def _goto_sleep(self):
        self._mode = ModesEnum.DESTROYED
        self.destroy()


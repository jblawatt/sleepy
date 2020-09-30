
from threading import Thread
from player import PlayerBase
from enum import Enum
from time import sleep
from datetime import datetime


class ModesEnum(Enum):
    ACTIVE = 0
    INACTIVE = 1
    RUNNING = 2



class WakeThread(Thread):

    _player: PlayerBase = None
    _wake_time: datetime = None
    _mode: ModesEnum = None

    # TODO: Wake Factory
    def __init__(self, player):
        super().__init__()
        self._player = player
        self._mode = ModesEnum.INACTIVE

    def activate(self, value: datetime = None):
        self._wake_time = value
        self._mode = ModesEnum.ACTIVE

    def deactivate(self):
        self._wake_time = None
        self._mode = ModesEnum.INACTIME

    def _is_active(self):
        return ModesEnum.ACTIVE == self._mode

    def _is_running(self):
        return ModesEnum.RUNNING == self._mode

    def run(self):
        while True:
            sleep(.5)
            if not self._is_active():
                continue
            if self._is_running():
                continue
            if self._wake_time < datetime.now():
                self._player.play()
                self._mode = ModesEnum.RUNNING



from threading import Thread, Event
from time import sleep
from datetime import datetime


class WakeThread(Thread):

    def __init__(self, player, wake_time, daemon=True):
        super().__init__(daemon=daemon)
        self._player = player
        self._wake_time = wake_time
        self._destroy = Event()

    def destroy(self):
        self._destroy.set()

    def is_playing(self):
        return self._player.is_playing()

    def run(self):
        while not self._destroy.is_set():
            sleep(.5)
            if not self._player.is_playing() and \
                    self._wake_time < datetime.now():
                print('time to wake up')
                self._player.play()
            else:
                if self._player.is_playing():
                    print('playing to wake up...')
                else:
                    td = self._wake_time - datetime.now()
                    print('will start in %s seconds (%s)' %
                         (td.seconds, self._wake_time))

        self._player.stop()
        self._player = None


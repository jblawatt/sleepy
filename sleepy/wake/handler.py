
from datetime import datetime, date
from dateutil import rrule

from sleepy.wake.thread import WakeThread
from sleepy.player import player_factory
from sleepy import config


class WakeHandler:

    _wake_thread = None
    _is_active = False

    def __init__(self):
        self._is_active = False

    def get_wake_time(self):
        c = config.get()
        t = c.get('wake', 'time')
        dtstart = datetime.combine(
            date.today(),
            datetime.strptime(t, '%H:%M').time()
        )
        for wt in rrule.rrule(rrule.DAILY, dtstart=dtstart):
            if wt > datetime.now():
                return wt

    def is_playing(self):
        if self._wake_thread:
            return self._wake_thread.is_playing()
        return False

    def toggle(self):
        if self._is_active:
            self._wake_thread.destroy()
            self._wake_thread.join()
            self._wake_thread = None
            self._is_active = False
        else:
            wake_time = self.get_wake_time()
            player_name = config.get().get('wake', 'player')
            player = player_factory(player_name)
            self._wake_thread = WakeThread(player, wake_time)
            self._wake_thread.start()
            self._is_active = True

    def is_active(self) -> bool:
        return self._is_active

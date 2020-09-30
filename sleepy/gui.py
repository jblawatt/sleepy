
from tkinter import *
from datetime import datetime
from player import VLCPlayer
from sleep import SleepThread
from wake import WakeThread


class ActionEndlessIterator:

    actions = []
    _current = 0

    def __init__(self, *actions):
        self.actions = actions

    def __iter__(self):
        while True:
            for i in actions:
                yield self.__next__()

    def __next__(self):
        if len(self.actions) == 0:
            raise StopIteration()
        c = self._current
        self._current += 1
        try:
            return self.actions[c]
        except IndexError:
            self._current = 1
            return self.actions[0]

    def next(self):
        try:
            return self.actions[self._current + 1]
        except IndexError:
            return self.actions[0]


class SleepAction:

    def apply(self, sleep_thread):
        pass

    def get_text(self):
        pass


class StartSleepAction(SleepAction):

    _start_minutes: int = 0

    def __init__(self, start_minutes: int):
        self._start_minutes = start_minutes

    def apply(self, sleep_thread):
        sleep_thread.activate(self._start_minutes)

    def get_text(self):
        return 'start'


class StopSleepAction(SleepAction):

    def apply(self, sleep_thread):
        sleep_thread.deactivate()

    def get_text(self):
        return 'stop'

class SetTimeSleepAction(StartSleepAction):

    def get_text(self):
        return 'set %s' % self._start_minutes


class StartWakeAction:

    def apply(self, wake_thread):
        wake_thread.activate()

    def get_text(self):
        return 'start'

class StopWakeAction:

    def apply(self, wake_thread):
        wake_thread.deactivate()

    def get_text(self):
        return 'stop'


class Application:

    _root: Tk = None
    _frame: Frame = None

    _sleep_thread = None
    _sleep_action_toggle = ActionEndlessIterator(
        StartSleepAction(10),
        SetTimeSleepAction(20),
        SetTimeSleepAction(30),
        SetTimeSleepAction(40),
        StopSleepAction(),
    )

    _wake_thread = None
    _wake_action_toggle = ActionEndlessIterator(
        StartWakeAction(),
        StopWakeAction(),
    )


    def __init__(self):
        self._root = Tk()
        self._frame = Frame(self._root)

        self._sleep_button = Button(
                self._root,
                text='start (sleep)',
                width=15,
                command=self._on_sleep_button_click)

        self._sleep_button.pack()

        # TODO: Config / Player Factory
        self._sleep_player = VLCPlayer()
        self._sleep_thread = SleepThread(self._sleep_player)
        self._sleep_thread.daemon = True
        self._sleep_thread.start()

        self._wake_button = Button(
            self._root,
            text='start (wake)',
            width=15,
            command=self._on_wake_button_click
        )

        self._wake_button.pack()

        self._wake_player = VLCPlayer()
        self._wake_thread = WakeThread(self._wake_player)
        self._wake_thread.daemon = True
        self._wake_thread.start()

    def mainloop(self):
        self._root.mainloop()

    def _on_sleep_button_click(self):
        next_action = self._sleep_action_toggle.next()
        action = next(self._sleep_action_toggle)
        action.apply(self._sleep_thread)
        self._sleep_button['text'] = next_action.get_text()

    def _on_wake_button_click(self):
        next_action = self._wake_action_toggle.next()
        action = next(self._wake_action_toggle)
        action.apply(self._wake_thread)
        self._wake_button['text'] = next_action.get_text()


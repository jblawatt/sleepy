
from tkinter import Tk, Frame, Button
from sleepy.wake.handler import WakeHandler
from sleepy.sleep.handler import SleepHandler
from sleepy.sleep.thread import SleepEvents

# from sleepy.wake.thread import WakeThread


class Application:

    _root: Tk = None
    _frame: Frame = None

    def __init__(self):
        self._root = Tk()
        self._frame = Frame(self._root)

        self._sleep_button = Button(
            self._root,
            text='start (sleep)',
            width=15,
            command=self._on_sleep_button_click)

        self._sleep_button.pack()

        self._sleep_handler = SleepHandler()
        self._sleep_handler.connect_event(
            SleepEvents.DESTROYED, self._on_sleep_event)

        self._wake_button = Button(
            self._root,
            text='start (wake)',
            width=15,
            command=self._on_wake_button_click
        )

        self._wake_button.pack()

        self._wake_handler = WakeHandler()

    def _on_sleep_event(self, *args, **kwargs):
        self._refresh_button()

    def mainloop(self):
        self._root.mainloop()

    def _refresh_button(self):
        self._sleep_button['text'] = self._sleep_handler.next_message()

    def _on_sleep_button_click(self):
        self._sleep_handler.iter_sleep()
        self._refresh_button()

    def _on_wake_button_click(self):
        self._wake_handler.toggle()
        if self._wake_handler.is_active():
            text = 'active (%s)' % self._wake_handler.get_wake_time().time()
        else:
            text = 'start (wake)'
        self._wake_button['text'] = text


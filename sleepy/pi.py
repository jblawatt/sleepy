
from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
from player import VLCPlayer
from sleep import SleepThread


SLEEP_BUTTON = 11
SLEEP_LIGHT = 7

WAKE_BUTTON = -1
WAKE_LIGHT = -1


INTERVAL = .01

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SLEEP_LIGHT, GPIO.OUT)
GPIO.setup(SLEEP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class SleepActions(Enum):
    START = 1
    ADD_10 = 2
    ADD_20 = 3
    STOP = 4



class Sleepy:

    _sleep_thread = None
    _sleep_click_counter = 0

    def mainloop(self):
        print("go for it...")
        while True:
            sleep(INTERVAL)
            if not GPIO.input(SLEEP_BUTTON):
                self._on_sleep_button_action()
                sleep(1)
            if self._sleep_thread is not None and \
                    self._sleep_thread.is_destroyed():
                self._sleep_thread.destroy()
                self._sleep_thread = None
                self._sleep_click_counter = 0
                GPIO.output(SLEEP_LIGHT, GPIO.LOW)
                print("destroy sleep thread")

    def _on_sleep_button_action(self):
        if self._sleep_thread is None:
            print("new sleep thread")
            GPIO.output(SLEEP_LIGHT, GPIO.HIGH)
            self._sleep_thread = SleepThread(VLCPlayer())
            self._sleep_thread.daemon = True
            self._sleep_thread.start()
            self._sleep_thread.activate(10)
            self._sleep_click_counter = 2
        else:
            if self._sleep_click_counter > 5:
                print("quit sleep thread")
                self._sleep_thread.deactivate()
                self._sleep_thread.destroy()
                self._sleep_thread = None
                self._sleep_click_counter = 0
                GPIO.output(SLEEP_LIGHT, GPIO.LOW)
            else:
                print("increase sleep thread %s" % self._sleep_click_counter)
                self._sleep_thread.activate(self._sleep_click_counter * 10)
                self._sleep_click_counter += 1


if __name__ == '__main__':
    try:
        Sleepy().mainloop()
    finally:
        GPIO.cleanup()


import logging

try:
    import RPi.GPIO as GPIO
except ImportError:
    import sleepy.patches as p
    p.setup_dev_mode()


from time import sleep
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from sleepy.sleep.handler import SleepHandler
from sleepy.sleep.thread import SleepEvents
from sleepy.wake.handler import WakeHandler
import sleepy.pi_lcd as lcd

SLEEP_BUTTON = 11
SLEEP_LIGHT = 7

WAKE_BUTTON = 13
WAKE_LIGHT = 15

TIME_BUTTON = 23
DISPLAY_BUTTON = 21

INTERVAL = .01

GPIO.setmode(GPIO.BOARD)

GPIO.setup(SLEEP_LIGHT, GPIO.OUT)
GPIO.setup(WAKE_LIGHT, GPIO.OUT)
GPIO.setup(SLEEP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(WAKE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TIME_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(DISPLAY_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd.setup()

# GPIO.output(lcd.DISPLAY_E, GPIO.LOW)

_log_format = '%(asctim)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=_log_format)


class Application:

    _sleep_handler: SleepHandler = None
    _wake_handler: WakeHandler = None

    _sleep_well_message = None

    def __init__(self):
        self._sleep_handler = SleepHandler()
        self._sleep_handler.connect_event(SleepEvents.DESTROYED, self._on_sleep_event)
        # TODO: wake handler
        self._wake_handler = WakeHandler()

    def mainloop(self):
        try:
            self._mainloop()
        finally:
            GPIO.cleanup()

    def _mainloop(self):
        print("sleepy is ready to start...")

        lcd.init()
        lcd.lcd_string_1('SLEEP IS OFF')
        lcd.lcd_string_2('WAKE IS OFF')

        # reset
        for pin in (SLEEP_LIGHT, WAKE_LIGHT):
            GPIO.output(pin, GPIO.LOW)

        while True:
            # endlosscheilfe für das
            sleep(INTERVAL)
            if not GPIO.input(SLEEP_BUTTON):

                self._on_sleep_button_action()

                # nach jedem klick 1 sekunde warte, damit nicht
                # unnötig viele aktion ausgelöst werden
                # beim "gedrückhalten" werden damit alle 1 sekunde
                # neue aktionen ausgelöst
                sleep(1)

            if not GPIO.input(WAKE_BUTTON):
                self._on_wake_button_action()
                sleep(1)

            # if not GPIO.input(DISPLAY_BUTTON):
            #     GPIO.output(lcd.DISPLAY_E, True)
            #     print('display on')
            # else:
            #     GPIO.output(lcd.DISPLAY_E, False)
            #     sleep(1)

            if not GPIO.input(TIME_BUTTON):
                self._print_time()
            else:
                self._update_display_sleep()
                self._update_display_wake()

    def _print_time(self):
        now = datetime.now()
        d = now.strftime('%d.%m.%Y')
        h = now.strftime('%H:%M')
        lcd.lcd_string_1('   %s   ' % d)
        lcd.lcd_string_2('     %s     ' % h)

    def _update_display_sleep(self):
        h = self._sleep_handler
        if self._sleep_well_message is not None and \
                self._sleep_well_message > datetime.now():
            lcd.lcd_string_1('SLEEP WELL!')
            return
        if not h.is_active():
            lcd.lcd_string_1('SLEEP IS OFF')
        else:
            try:
                td, __ = str(h.sleep_timedelta()).rsplit('.')
            except TypeError:
                print("error")
            else:
                lcd.lcd_string_1('SLEEP IN %s' % td)

    def _update_display_wake(self):
        h = self._wake_handler
        if not h.is_active():
            lcd.lcd_string_2('WAKE IS OFF')
        else:
            if h.is_playing():
                lcd.lcd_string_2('WAKE UP!!')
            else:
                wake_time = h.get_wake_time()
                wake_time_str = wake_time.time().strftime('%H:%M')
                lcd.lcd_string_2('WAKE AT %s' % wake_time_str)

    def _on_sleep_event(self, *args, **kwargs):
        GPIO.output(SLEEP_LIGHT, GPIO.LOW)
        self._sleep_well_message = datetime.now() + timedelta(seconds=3)

    def _on_sleep_button_action(self):
        self._sleep_handler.iter_sleep()
        if self._sleep_handler.is_active():
            gpio_light_state = GPIO.HIGH
        else:
            gpio_light_state = GPIO.LOW
        GPIO.output(SLEEP_LIGHT, gpio_light_state)

    def _on_wake_button_action(self):
        self._wake_handler.toggle()
        if self._wake_handler.is_active():
            gpio_light_state = GPIO.HIGH
        else:
            gpio_light_state = GPIO.LOW
        GPIO.output(WAKE_LIGHT, gpio_light_state)


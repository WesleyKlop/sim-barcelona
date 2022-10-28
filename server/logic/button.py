import logging as log
from os.path import abspath, basename
from threading import Lock, Thread, Timer
from time import time

import RPi.GPIO as GPIO

from server.logic.announcer import announcer
from server.logic.camera import take_picture
from server.logic.image import ImageGenerator


class ButtonHandler(Thread):
    def __init__(self, pin, func, edge='both', bounce_time=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bounce_time = float(bounce_time) / 1000

        self.last_pinval = GPIO.input(self.pin)
        self.lock = Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = Timer(self.bounce_time, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.last_pinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.last_pinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.last_pinval = pinval
        self.lock.release()


def do_the_thing(_pin):
    log.info('Starting a run')
    announcer.sse('running', 'phase')
    generator = ImageGenerator()
    announcer.log('Got button press')

    img_path = take_picture(abspath('public/results'))
    if img_path is None:
        announcer.log('Failed to take picture')
        return None

    announcer.sse('/results/' + basename(img_path), 'image')
    announcer.log('Got picture')

    result = generator.generate(img_path, abspath('public/results'))
    announcer.log('Generated picture')
    announcer.sse('/results/' + result, 'image')
    announcer.sse('finished', 'phase')


BUTTON_PIN = 7


def setup():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    cb = ButtonHandler(BUTTON_PIN, do_the_thing, edge='rising', bounce_time=100)
    cb.start()
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=cb)

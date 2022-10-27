import logging as log
import os
from os.path import abspath, basename, exists
from tempfile import gettempdir
from threading import Lock

import RPi.GPIO as GPIO

from server.logic.announcer import announcer
from server.logic.camera import take_picture
from server.logic.image import ImageGenerator

BUTTON_PIN = 7


def do_the_thing():
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


def setup(lock: Lock):
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def callback(evt):
        announcer.log('Button callback')
        if not lock.acquire(blocking=False):
            announcer.log('Dropping button press')
            return
        try:
            do_the_thing()
        finally:
            lock.release()

    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=callback)

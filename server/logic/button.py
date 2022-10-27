import os.path
from threading import Lock

import RPi.GPIO as GPIO
import flask

from server.logic.announcer import announcer, format_sse
from server.logic.camera import take_picture
from server.logic.image import ImageGenerator

BUTTON_PIN = 7

mutex = Lock()


def do_the_thing():
    announcer.log('Got button press')
    generator = ImageGenerator()
    announcer.log('Created image generator')

    img_path = take_picture(os.path.abspath('public/results'))
    announcer.announce(
        format_sse(flask.url_for('static', filename='results/' + os.path.basename(img_path)), 'start'))
    if img_path is None:
        announcer.log('Failed to take picture')
        return None
    announcer.log('Got picture')

    result = generator.generate(img_path, os.path.abspath('public/results'))
    announcer.announce(
        format_sse(flask.url_for('static', filename='results/' + result), 'result')
    )


def callback(evt):
    if mutex.locked():
        return
    try:
        mutex.acquire(blocking=True)
        do_the_thing()
    finally:
        mutex.release()


def setup(cb=callback):
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=cb)

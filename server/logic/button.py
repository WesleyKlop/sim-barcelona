from os.path import abspath, basename

import RPi.GPIO as GPIO
import flask

from server.logic.announcer import announcer
from server.logic.camera import take_picture
from server.logic.image import ImageGenerator

BUTTON_PIN = 7

# Lock
is_running = False


def do_the_thing():
    announcer.log('Got button press')
    generator = ImageGenerator()
    announcer.log('Created image generator')

    img_path = take_picture(abspath('public/results'))
    announcer.sse(flask.url_for('static', filename='results/' + basename(img_path)), 'start')

    if img_path is None:
        announcer.log('Failed to take picture')
        return
    announcer.log('Got picture')

    result = generator.generate(img_path, abspath('public/results'))
    announcer.sse(flask.url_for('static', filename='results/' + result), 'result')


def callback(evt):
    global is_running
    if is_running is True:
        return
    is_running = True
    try:
        do_the_thing()
    finally:
        is_running = False


def setup(cb=callback):
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=cb)

from os.path import abspath, basename
from threading import Lock
from time import time

import RPi.GPIO as GPIO

from server.logic.announcer import announcer
from server.logic.camera import take_picture
from server.logic.image import ImageGenerator

BUTTON_PIN = 7

last_timestamp = 0


def setup(mutex: Lock):
    announcer.log(msg=f"Running setup. Mutex: {mutex.locked()}")
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def callback(evt):
        global last_timestamp
        announcer.log(f'Button press: detected. Mutex lock state: {mutex.locked()}.')

        announcer.log(last_timestamp)
        if time() - last_timestamp < 60:
            announcer.log('Cancelling because of debounce')
            return

        if not mutex.acquire(blocking=False):
            announcer.log('Button press: cancelling')
            return
        try:
            announcer.log("Button press: accepted. Generating image.")
            generate_image()
        finally:
            mutex.release()

    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=callback, bouncetime=200)


def generate_image():
    global last_timestamp
    last_timestamp = time()
    announcer.log('------Generating image...')
    announcer.sse('running', 'phase')
    generator = ImageGenerator()
    announcer.log('made image generator')

    img_path = take_picture(abspath('public/results'))
    if img_path is None:
        announcer.log('Failed to take picture')
        return None
    announcer.sse('/results/' + basename(img_path), 'image')
    announcer.log('Image successfully taken.')

    result = generator.generate(img_path, abspath('public/results'))
    announcer.log('Generated picture')
    announcer.sse('/results/' + result, 'image')
    announcer.sse('finished', 'phase')

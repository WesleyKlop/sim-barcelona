from time import sleep

from cv2 import VideoCapture, imwrite

from .announcer import announcer
from .fs import generate_random_filepath


def take_picture(dest_dir: str = None):
    announcer.log('Going to take a pic')
    cam = VideoCapture(0)
    # Take picture using usb webcam
    # Returns the path to the picture
    sleep(5)
    announcer.log('Slept')
    s, img = cam.read()
    announcer.log('Picture taken')
    if s:
        # Save the image
        path = generate_random_filepath(dest_dir)
        imwrite(path, img)
        announcer.log('Picture written to ' + path)
        return path

    print("Picture capture error")
    return None

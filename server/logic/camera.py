from time import sleep

from cv2 import VideoCapture, imwrite

from .announcer import announcer
from .fs import generate_random_filepath


def take_picture(dest_dir: str = None):
    announcer.log('Selecting imaging device.')
    cam = VideoCapture(0)
    # Take picture using usb webcam
    # Returns the path to the picture
    sleepTime = 2
    announcer.log(f'Sleeping {sleepTime} seconds...')
    sleep(sleepTime)
    announcer.log('Taking image...')
    s, img = cam.read()
    announcer.log('Image taken.')
    if s:
        # Save the image
        path = generate_random_filepath(dest_dir)
        imwrite(path, img)
        announcer.log('Image written to ' + path)
        return path

    print("Error in taking image.")
    return None

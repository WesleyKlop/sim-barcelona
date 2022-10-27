from cv2 import VideoCapture, imwrite

from .fs import generate_random_filepath


def take_picture():
    # Take picture using usb webcam
    # Returns the path to the picture
    cam = VideoCapture(0)
    s, img = cam.read()
    if s:
        # Save the image
        path = generate_random_filepath()
        imwrite(path, img)
        print(path)
        return path
    else:
        print("Picture capture error")

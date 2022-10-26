from .camera import take_picture
from .image import generate_stylized_image


def do_the_thing():
    content_image_path = take_picture()
    stylized_image = generate_stylized_image(content_image_path)
    print(stylized_image)
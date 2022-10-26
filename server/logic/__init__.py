from .camera import take_picture
from .image import generate_stylized_image

def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


def do_the_thing():
    content_image_path = take_picture()
    stylized_image_path = generate_stylized_image(content_image_path)
    print(stylized_image_path)
    pass
from .camera import take_picture
from .image import ImageGenerator

def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg

def do_the_thing():
    content_image_path = take_picture()
    stylized_image_path = generator.generate(content_image_path)
    print(stylized_image_path)
    pass
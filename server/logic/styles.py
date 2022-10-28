from os.path import abspath
from random import choice

styles = [
    'gaudi_1.jpeg',
    'picasso_1.png',
]


def get_random_style_image() -> str:
    style = choice(styles)
    return abspath('public/assets/' + style)

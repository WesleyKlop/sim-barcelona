from os.path import abspath
from random import choice

styles = [
    'gaudi_1.jpeg',
    'gaudi_2.jpeg',
    'gaudi_3.jpg',
    'picasso_1.png',
    'picasso_2.jpeg',
]


def get_random_style_image() -> str:
    style = choice(styles)
    return abspath('public/assets/' + style)

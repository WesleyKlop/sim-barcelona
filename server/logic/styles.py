from os.path import abspath
from random import choice

styles = [
    'gaudi_1.jpeg',
    'dali_1.jpg',
    'picasso_1.png',
    'gaudi_2.jpeg',
    'picasso_2.jpeg',
    'dali_2.jpeg',
    'gaudi_3.jpg',
    'picasso_3.jpeg',
    'dali_3.jpeg',
]


def get_random_style_image() -> str:
    style = choice(styles)
    return abspath('public/assets/' + style)

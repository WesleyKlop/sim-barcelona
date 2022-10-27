from os.path import join
from tempfile import gettempdir
from uuid import uuid4


def generate_random_filepath(parent_dir: str = gettempdir()) -> str:
    return join(parent_dir, str(uuid4()) + '.png')

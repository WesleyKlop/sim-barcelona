import os
import tempfile
import uuid


def generate_random_filepath() -> str:
    return os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + '.png')

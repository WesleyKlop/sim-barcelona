import functools

import tensorflow as tf
import tensorflow_hub as hub

from .styles import get_random_style_image
from .fs import generate_random_filepath


IMAGE_SIZE_OUTPUT = 512
IMAGE_SIZE_CONTENT = (IMAGE_SIZE_OUTPUT, IMAGE_SIZE_OUTPUT)
# The style prediction model was trained with image size 256 and it's the
# recommended image size for the style image (though, other sizes work as
# well but will lead to different results).
IMAGE_SIZE_STYLE = (256, 256)

HUB_MODULE = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'

class ImageGenerator:
    def __init__(self):
        self.model = None

    def generate(self, image_path: str) -> str:
        if self.model == None:
            print("Loading hub model")
            self.model = hub.load(HUB_MODULE)

        image_path = self.load_image(image_path, IMAGE_SIZE_CONTENT)
        style_image = self.load_image(get_random_style_image(), IMAGE_SIZE_STYLE)
        style_image = tf.nn.avg_pool(
            style_image,
            ksize=[3, 3],
            strides=[1, 1],
            padding='SAME'
        )
        outputs = self.model(
            tf.constant(image_path),
            tf.constant(style_image)
        )

        outFile = generate_random_filepath()
        # Write the generated image tensor to the outFile
        tf.io.write_file(outFile, tf.image.encode_png(outputs[0]))

        return outFile

    def crop(image):
        """Returns a cropped square image."""
        shape = image.shape
        new_shape = min(shape[1], shape[2])
        offset_y = max(shape[1] - shape[2], 0) // 2
        offset_x = max(shape[2] - shape[1], 0) // 2
        return tf.image.crop_to_bounding_box(
            image,
            offset_y, offset_x,
            new_shape, new_shape
        )

    @functools.lru_cache(maxsize=None)
    def load_image(image_path: str, image_size=(256, 256), preserve_aspect_ratio=True):
        """Loads and preprocesses images."""
        # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
        img = tf.io.decode_image(
            tf.io.read_file(image_path),
            channels=3,
            dtype=tf.float32
        )[tf.newaxis, ...]

        img = self.crop(img)  # TODO: maybe this can be removed?
        img = tf.image.resize(img, image_size, preserve_aspect_ratio)
        return img

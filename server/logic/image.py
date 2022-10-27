import functools

import tensorflow as tf

from .fs import generate_random_filepath
from .styles import get_random_style_image

IMAGE_SIZE_OUTPUT = 384
IMAGE_SIZE_CONTENT = (IMAGE_SIZE_OUTPUT, IMAGE_SIZE_OUTPUT)
# The style prediction model was trained with image size 256, and it's the
# recommended image size for the style image (though, other sizes work as
# well but will lead to different results).
IMAGE_SIZE_STYLE = (256, 256)


class ImageGenerator:
    def __init__(self):
        self.predict_path = tf.keras.utils.get_file(
            'style_predict.tflite',
            'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/prediction/1?lite-format=tflite'
        )
        self.transform_path = tf.keras.utils.get_file(
            'style_transform.tflite',
            'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/transfer/1?lite-format=tflite'
        )

    def predict(self, style_image):
        # Load the model.
        interpreter = tf.lite.Interpreter(model_path=self.predict_path)

        # Set model input.
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        interpreter.set_tensor(input_details[0]["index"], style_image)

        # Calculate style bottleneck.
        interpreter.invoke()
        return interpreter.tensor(
            interpreter.get_output_details()[0]["index"]
        )()

    def transform(self, content_image, style_bottleneck):
        # Load the model.
        interpreter = tf.lite.Interpreter(model_path=self.transform_path)

        # Set model input.
        input_details = interpreter.get_input_details()
        interpreter.allocate_tensors()

        # Set model inputs.
        interpreter.set_tensor(input_details[0]["index"], content_image)
        interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
        interpreter.invoke()

        # Transform content image.
        return interpreter.tensor(
            interpreter.get_output_details()[0]["index"]
        )()

    def generate(self, image_path: str) -> str:
        content_image = self.load_image(image_path, IMAGE_SIZE_CONTENT)
        style_image = self.load_image(
            get_random_style_image(),
            IMAGE_SIZE_STYLE
        )

        style_bottleneck = self.predict(style_image)
        stylized_image = self.transform(content_image, style_bottleneck)

        out_file = generate_random_filepath()
        # Write the generated image tensor to the outFile
        tf.io.write_file(
            out_file,
            tf.image.encode_png(
                tf.squeeze(
                    tf.image.convert_image_dtype(stylized_image, dtype=tf.uint8)
                )
            )
        )

        return out_file

    def crop(self, image):
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
    def load_image(self, image_path: str, image_size=(256, 256), preserve_aspect_ratio=True):
        """Loads and preprocesses images."""
        # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
        img = tf.io.decode_image(
            tf.io.read_file(image_path),
            channels=3,
            dtype=tf.float32
        )[tf.newaxis, ...]

        img = self.crop(img)  # TODO: maybe this can be removed?
        img = tf.image.resize(
            img, image_size, preserve_aspect_ratio=preserve_aspect_ratio)
        return img

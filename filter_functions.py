import cv2
import numpy as np
from PIL import Image, ImageTk


def apply_sepia(canvas, original_image):
    if original_image is not None:
        kernel = np.array([[0.393, 0.769, 0.189],
                           [0.349, 0.686, 0.168],
                           [0.272, 0.534, 0.131]])
        sepia_image = cv2.transform(original_image, kernel)
        # return filtered_image
        return display_image(canvas, sepia_image)


def apply_black_and_white(canvas, original_image):
    if original_image is not None:
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
        bw_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        # return bw_image
        return display_image(canvas, bw_image)


def apply_brighten(canvas, original_image):
    if original_image is not None:
        brightness_factor = 3
        # Convert the image to a floating point representation
        original_image_float = original_image.astype(np.float32)

        # Scale the image by the brightness factor
        brightened_image_float = original_image_float * brightness_factor

        # Clip the pixel values to ensure they remain in the valid range [0, 255]
        brightened_image_float = np.clip(brightened_image_float, 0, 255)

        # Convert the image back to the uint8 data type (expected by OpenCV)
        brightened_image_uint8 = brightened_image_float.astype(np.uint8)

        return display_image(canvas, brightened_image_uint8)


def display_image(canvas, image):
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, anchor='nw', image=image)

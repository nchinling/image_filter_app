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


def apply_blur(canvas, original_image):
    if original_image is not None:
        blur_image = cv2.blur(original_image, (5, 5))
        # return blur_image
        return display_image(canvas, blur_image)


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


def apply_cartoonisation(canvas, original_image):
    if original_image is not None:
        # Convert image to grayscale
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        # Apply median blur to smooth image
        blurred_image = cv2.medianBlur(gray_image, 7)
        # Detect edges using Canny edge detector
        edges = cv2.Canny(blurred_image, 100, 200)
        # Create a binary mask for the edges
        _, mask = cv2.threshold(edges, 70, 255, cv2.THRESH_BINARY_INV)
        # Combine the edges with the original image using bitwise and
        cartoon_image = cv2.bitwise_and(
            original_image, original_image, mask=mask)
        # return cartoon_image
        return display_image(canvas, cartoon_image)


def apply_oil_painting_effect(canvas, original_image):
    radius = 10
    intensity = 7
    if original_image is not None:
        # Convert image to grayscale
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        # Apply median blur to the grayscale image
        blurred_image = cv2.medianBlur(gray_image, 7)

        # Initialize output image
        oil_painting_image = np.zeros_like(original_image)

        # Apply oil painting effect
        for y in range(0, original_image.shape[0] - radius, radius):
            for x in range(0, original_image.shape[1] - radius, radius):
                roi = blurred_image[y:y+radius, x:x+radius]
                median = np.median(roi)
                oil_painting_image[y:y+radius, x:x+radius, 0][roi >=
                                                              median-intensity] = roi[roi >= median-intensity]
                oil_painting_image[y:y+radius, x:x+radius, 1][roi >=
                                                              median-intensity] = roi[roi >= median-intensity]
                oil_painting_image[y:y+radius, x:x+radius, 2][roi >=
                                                              median-intensity] = roi[roi >= median-intensity]
                oil_painting_image[y:y+radius, x:x+radius,
                                   0][roi < median-intensity] = median
                oil_painting_image[y:y+radius, x:x+radius,
                                   1][roi < median-intensity] = median
                oil_painting_image[y:y+radius, x:x+radius,
                                   2][roi < median-intensity] = median

        # return oil_painting_image
        return display_image(canvas, oil_painting_image)


def display_image(canvas, image):
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, anchor='nw', image=image)

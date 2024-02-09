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


def apply_pixelate(canvas, original_image, pixel_size=40):
    # Get the dimensions of the image
    height, width = original_image.shape[:2]

    # Resize the image to a smaller size
    small_image = cv2.resize(
        original_image, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)

    # Resize the small image back to the original size
    pixelated_image = cv2.resize(
        small_image, (width, height), interpolation=cv2.INTER_NEAREST)

    return display_image(canvas, pixelated_image)


# def apply_cartoonisation(canvas, original_image):
#     if original_image is not None:
#         # Convert image to grayscale
#         gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
#         # Apply median blur to smooth image
#         blurred_image = cv2.medianBlur(gray_image, 7)
#         # Detect edges using Canny edge detector
#         edges = cv2.Canny(blurred_image, 100, 200)
#         # Create a binary mask for the edges
#         _, mask = cv2.threshold(edges, 70, 255, cv2.THRESH_BINARY_INV)
#         # Combine the edges with the original image using bitwise and
#         cartoon_image = cv2.bitwise_and(
#             original_image, original_image, mask=mask)
#         # return cartoon_image
#         return display_image(canvas, cartoon_image)

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
        # Create a blank image to fill with ink effect
        ink_effect = cv2.cvtColor(blurred_image, cv2.COLOR_GRAY2BGR)
        # Combine the edges with the ink effect using bitwise and
        cartoon_image = cv2.bitwise_and(ink_effect, ink_effect, mask=mask)
        # return cartoon_image
        return display_image(canvas, cartoon_image)


def apply_oil_painting_effect(canvas, original_image, radius=8, intensity=7):
    if original_image is not None:
        # Initialize output image as a copy of the original image
        oil_painting_image = original_image.copy()

        # Apply oil painting effect
        for y in range(0, original_image.shape[0] - radius, radius):
            for x in range(0, original_image.shape[1] - radius, radius):
                roi = original_image[y:y+radius, x:x+radius]

                for c in range(3):  # Iterate over color channels (B, G, R)
                    median = np.median(roi[:, :, c])
                    oil_painting_image[y:y+radius, x:x+radius, c][roi[:, :, c] >=
                                                                  median-intensity] = roi[:, :, c][roi[:, :, c] >= median-intensity]
                    oil_painting_image[y:y+radius, x:x+radius,
                                       c][roi[:, :, c] < median-intensity] = median

    return display_image(canvas, oil_painting_image)


def apply_rotate(canvas, original_image, angle=90):

    # Rotate the original image by the specified angle
    rows, cols, _ = original_image.shape
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_image = cv2.warpAffine(
        original_image, rotation_matrix, (cols, rows))

    return display_image(canvas, rotated_image)


def display_image(canvas, image):
    # Convert numpy array to PIL Image
    image_pil = Image.fromarray(image)

    # Convert PIL Image to PhotoImage
    image_tk = ImageTk.PhotoImage(image_pil)
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    canvas.image = image_tk

    # Get the dimensions of the image
    image_width = image_pil.width
    image_height = image_pil.height

    # Calculate coordinates to place the image at the center of the canvas
    x = (canvas_width - image_width) // 2
    y = (canvas_height - image_height) // 2

    # Create image on canvas
    canvas.create_image(x, y, anchor='nw', image=image_tk)

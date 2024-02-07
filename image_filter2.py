import cv2
import numpy as np
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from filter_functions import apply_black_and_white, apply_sepia


CANVAS_HEIGHT = 500
CANVAS_WIDTH = 500


class ImageFilterApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Image Filter App")
        self.label = Label(self.root, text="This is cool!").pack()

        self.original_image = None
        self.filtered_image = None

        self.canvas = Canvas(self.root, width=CANVAS_WIDTH,
                             height=CANVAS_HEIGHT)
        self.canvas.pack()

        # self.sepia_button = Button(
        #     self.root, text="Sepia", command=self.apply_sepia)
        # self.sepia_button.pack(side=LEFT, padx=10)

        # self.bw_button = Button(
        #     self.root, text="Black & White", command=self.apply_black_and_white)
        # self.bw_button.pack(side=LEFT)

        self.sepia_button = Button(
            self.root, text="Sepia", command=lambda: apply_sepia(self.original_image))
        self.sepia_button.pack(side=LEFT, padx=10)

        self.bw_button = Button(
            self.root, text="Black & White", command=lambda: apply_black_and_white(self.original_image))
        self.bw_button.pack(side=LEFT)

        self.load_button = Button(
            self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(side=LEFT, padx=10)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        # convert from BGR scheme (Open CV) to RGB (PIL) if path available.
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(
                self.original_image, cv2.COLOR_BGR2RGB)

            # Resize the image to fit within the canvas
            canvas_width = CANVAS_WIDTH
            canvas_height = CANVAS_HEIGHT
            image_height, image_width, _ = self.original_image.shape
            if image_width > canvas_width or image_height > canvas_height:
                scale = min(canvas_width / image_width,
                            canvas_height / image_height)
                self.original_image = cv2.resize(
                    self.original_image, None, fx=scale, fy=scale)

            self.display_image(self.original_image)

    # def apply_sepia(self):
    #     if self.original_image is not None:
    #         kernel = np.array([[0.393, 0.769, 0.189],
    #                            [0.349, 0.686, 0.168],
    #                            [0.272, 0.534, 0.131]])
    #         self.filtered_image = cv2.transform(self.original_image, kernel)
    #         self.display_image(self.filtered_image)

    # def apply_black_and_white(self):
    #     if self.original_image is not None:
    #         self.filtered_image = cv2.cvtColor(
    #             self.original_image, cv2.COLOR_RGB2GRAY)
    #         self.filtered_image = cv2.cvtColor(
    #             self.filtered_image, cv2.COLOR_GRAY2RGB)
    #         self.display_image(self.filtered_image)

    def display_image(self, image):
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.canvas.image = image
        self.canvas.create_image(0, 0, anchor='nw', image=image)

# root = Tk()
# app = ImageFilterApp(root)
# root.mainloop()


window = Tk()
app = ImageFilterApp(window)
# pack is used to show the object in the window
# label = Label(
#     window, text="Welcome to the best Image Filter app!").pack()
window.mainloop()

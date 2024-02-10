import cv2
import numpy as np
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from filter_functions import *
import os


CANVAS_HEIGHT = 700
CANVAS_WIDTH = 700


class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter App")

        self.original_image = None
        self.filtered_image = None
        self.filename = None

        self.label = Label(self.root, text="", bg="#D04848")
        self.label.pack(side="top")

        self.frame = Frame(self.root, bg="#D04848")
        self.frame.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame, width=CANVAS_WIDTH,
                             height=CANVAS_HEIGHT, bg="#D04848", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.create_button("Sepia", lambda: apply_sepia(
            self.canvas, self.original_image))
        self.create_button("Black & White", lambda: apply_black_and_white(
            self.canvas, self.original_image))
        self.create_button("Brighten", lambda: apply_brighten(
            self.canvas, self.original_image))
        self.create_button("Pixelate", lambda: apply_pixelate(
            self.canvas, self.original_image))
        self.create_button("Invert", lambda: apply_invert(
            self.canvas, self.original_image))
        self.create_button("Load Image", self.load_image)
        self.create_button("Reset", self.reset_image)
        self.create_button("Emboss", lambda: apply_emboss(
            self.canvas, self.original_image))
        self.create_button("Blur", lambda: apply_blur(
            self.canvas, self.original_image))
        self.create_button("Ink", lambda: apply_ink(
            self.canvas, self.original_image))
        self.create_button("Oil Paint", lambda: apply_oil_painting_effect(
            self.canvas, self.original_image))

    def create_button(self, text, command):
        button = Button(
            self.root, text=text, command=command, fg="#FF004D", font=("Helvetica", 15), width=6, height=40
        )
        button.pack(side="left", padx=10, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        # convert from BGR scheme (Open CV) to RGB (PIL) if path available.
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(
                self.original_image, cv2.COLOR_BGR2RGB)

            self.filename = os.path.basename(file_path)
            self.update_label_text()

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

    def update_label_text(self):
        self.label.config(text=self.filename)

    def reset_image(self):
        self.canvas.delete("all")
        self.display_image(self.original_image)

    def display_image(self, image):
        # Convert numpy array to PIL Image
        image_pil = Image.fromarray(image)

        # Convert PIL Image to PhotoImage
        image_tk = ImageTk.PhotoImage(image_pil)
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        self.canvas.image = image_tk

        # Get the dimensions of the image
        image_width = image_pil.width
        image_height = image_pil.height

        # Calculate coordinates to place the image at the center of the canvas
        x = (canvas_width - image_width) // 2
        y = (canvas_height - image_height) // 2

        # Create image on canvas
        self.canvas.create_image(x, y, anchor='nw', image=image_tk)


window = Tk()
window.configure(bg="#D04848")
app = ImageFilterApp(window)
window.mainloop()

from tkinter import Button, LEFT


def create_sepia_button(root, command):
    sepia_button = Button(root, text="Sepia", command=command)
    sepia_button.pack(side=LEFT, padx=10)
    return sepia_button


def create_bw_button(root, command):
    bw_button = Button(root, text="Black & White", command=command)
    bw_button.pack(side=LEFT)
    return bw_button


def create_load_button(root, command):
    load_button = Button(root, text="Load Image", command=command)
    load_button.pack(side=LEFT, padx=10)
    return load_button

from PIL import Image, ImageTk
import tkinter as tk
import time
import nltk
from nltk.corpus import cmudict

# Ensure you have the necessary resources
nltk.download("cmudict")
pron_dict = cmudict.dict()


def remove_numbers(string):
    numbers_to_remove = ["0", "1", "3"]
    cleaned_string = "".join(char for char in string if char not in numbers_to_remove)
    return cleaned_string


def text_to_phonetic(text):
    words = text.lower().split()
    phonetic_string = remove_numbers(
        " ".join(
            " ".join(pron_dict[word][0]) if word in pron_dict else "OOV"
            for word in words
        )
    )
    return phonetic_string


def phonetic_to_shapes(phonetic_string):
    mouth_list = {
        "AA": "D",
        "AE": "C",
        "AH": "C",
        "AO": "E",
        "AW": "E",
        "AY": "E",
        "B": "A",
        "CH": "B",
        "D": "B",
        "DH": "B",
        "EH": "C",
        "ER": "E",
        "EY": "E",
        "F": "G",
        "G": "B",
        "HH": "H",
        "IH": "C",
        "IY": "B",
        "JH": "B",
        "K": "B",
        "L": "H",
        "M": "A",
        "N": "B",
        "NG": "B",
        "OW": "F",
        "OY": "F",
        "P": "A",
        "R": "B",
        "S": "B",
        "SH": "B",
        "T": "B",
        "TH": "B",
        "UH": "E",
        "UW": "F",
        "V": "G",
        "W": "F",
        "Y": "B",
        "Z": "B",
        "ZH": "B",
        "OOV": "X",
    }
    return [mouth_list.get(phon, "X") for phon in phonetic_string.split()]


# Set up the display window
root = tk.Tk()

# Define paths to your images
image_paths = {
    "A": "vermouth/ver-A.png",
    "B": "vermouth/ver-B.png",
    "C": "vermouth/ver-C.png",
    "D": "vermouth/ver-D.png",
    "E": "vermouth/ver-E.png",
    "F": "vermouth/ver-F.png",
    "G": "vermouth/ver-G.png",
    "H": "vermouth/ver-H.png",
    "X": "vermouth/ver-X.png",
}

# Load images and prepare for display after root is initialized
images = {shape: Image.open(path) for shape, path in image_paths.items()}
tk_images = {shape: ImageTk.PhotoImage(image) for shape, image in images.items()}

label = tk.Label(root)
label.pack()

text_entry = tk.Entry(root, width=50)
text_entry.pack()


def display_image(shape):
    label.config(image=tk_images[shape])
    root.update()
    time.sleep(0.18)


def animate_from_text():
    user_text = text_entry.get()
    phonetic = text_to_phonetic(user_text)
    shapes = phonetic_to_shapes(phonetic)
    for shape in shapes:
        display_image(shape)
    time.sleep(1)
    display_image("X")


animate_button = tk.Button(root, text="Animate Text", command=animate_from_text)
animate_button.pack()

root.mainloop()

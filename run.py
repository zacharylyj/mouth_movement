from PIL import Image, ImageTk
import tkinter as tk
import time
import speech_recognition as sr
import nltk
from nltk.corpus import cmudict

# Ensure you have the necessary resources
nltk.download("cmudict")
pron_dict = cmudict.dict()

# Initialize the speech recognizer and microphone
recognizer = sr.Recognizer()
mic = sr.Microphone()


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
    mouth_list = [
        ["AA", "D"],
        ["AE", "C"],
        ["AH", "C"],
        ["AO", "E"],
        ["AW", "E"],
        ["AY", "E"],
        ["B", "A"],
        ["CH", "B"],
        ["D", "B"],
        ["DH", "B"],
        ["EH", "C"],
        ["ER", "E"],
        ["EY", "E"],
        ["F", "G"],
        ["G", "B"],
        ["HH", "H"],
        ["IH", "C"],
        ["IY", "B"],
        ["JH", "B"],
        ["K", "B"],
        ["L", "H"],
        ["M", "A"],
        ["N", "B"],
        ["NG", "B"],
        ["OW", "F"],
        ["OY", "F"],
        ["P", "A"],
        ["R", "B"],
        ["S", "B"],
        ["SH", "B"],
        ["T", "B"],
        ["TH", "B"],
        ["UH", "E"],
        ["UW", "F"],
        ["V", "G"],
        ["W", "F"],
        ["Y", "B"],
        ["Z", "B"],
        ["ZH", "B"],
        ["OOV", "X"],
    ]
    mouth_movements = []
    for phoneme in phonetic_string.split():
        found = False
        for pair in mouth_list:
            if phoneme == pair[0]:
                mouth_movements.append(pair[1])
                found = True
                break
        if not found:
            mouth_movements.append("M")
    return mouth_movements


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


def display_image(shape):
    label.config(image=tk_images[shape])
    root.update()
    time.sleep(0.2)


def display_resting_image():
    display_image("X")
    root.update()


def add_transition_shapes(phonetic):
    transitions = {
        ("A", "D"): ["A", "C", "D"],
        ("B", "D"): ["B", "C", "D"],
        ("C", "F"): ["C", "E", "F"],
        ("D", "F"): ["D", "E", "F"],
    }
    result = []
    i = 0
    while i < len(phonetic) - 1:
        current_shape = phonetic[i]
        next_shape = phonetic[i + 1]
        if (current_shape, next_shape) in transitions:
            result.extend(transitions[(current_shape, next_shape)])
            i += 1
        else:
            result.append(current_shape)
        i += 1
    if i == len(phonetic) - 1:
        result.append(phonetic[-1])
    return result


def main():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=0.3, phrase_time_limit=5.0)
                text = recognizer.recognize_google(audio)
                if text:
                    phonetic = text_to_phonetic(text)
                    print(
                        f"------------------------------\n{text} ->\n{phonetic}\n------------------------------"
                    )
                    enhanced_phonetic = add_transition_shapes(phonetic)
                    for shape in enhanced_phonetic:
                        display_image(shape)
                else:
                    display_resting_image()
            except sr.WaitTimeoutError:
                display_resting_image()
            except sr.UnknownValueError:
                display_resting_image()
                print("Could not understand audio")
            except Exception as e:
                print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()

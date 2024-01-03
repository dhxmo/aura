import os
import threading
import tkinter as tk
import requests
from PIL import ImageTk, Image

from core.speech_recognition import SpeechRecognitionApp
from parser.config import Config


def init_app():
    root = tk.Tk()
    root.title('Aura')
    root.geometry('500x250')
    root.configure(background='black')

    # Load an image using PIL
    logo_image = Image.open(os.path.join(os.getcwd(), 'assets', 'logo', 'logo.png'))
    photo_image = ImageTk.PhotoImage(logo_image)
    label1 = tk.Label(image=photo_image)
    label1.image = photo_image
    label1.place(x=0, y=0)

    try:
        requests.head("http://www.google.com/", timeout=Config.timeout)

        # TODO: add a Aura server check. needs to be a paid user

        # TODO: check user. only allow one session per email

        # TODO: check for updates mechanism

        # Create a thread for recognizing speech
        sr = SpeechRecognitionApp()
        speech_thread = threading.Thread(target=sr.run)
        speech_thread.start()

    except requests.ConnectionError:
        # TODO: write these on screen and add text to speech
        print("The internet connection is down. Please reconnect and restart this app")

    root.mainloop()


if __name__ == '__main__':
    init_app()

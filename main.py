import threading
import tkinter as tk
import requests

from core.speech_recognition import SpeechRecognitionApp
from parser.config import Config


def init_app():
    root = tk.Tk()
    root.title('Aura')
    root.geometry('500x250')

    # Check internet connection

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
        print("The internet connection is down. Please reconnect and restart this app")
        # Display error message in DearPyGUI viewport
        # with dpg.window(label="Error"):
        #     dpg.add_text("The internet connection is down. Please reconnect and restart this app")

    root.mainloop()


if __name__ == '__main__':
    init_app()

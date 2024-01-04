import threading
import tkinter as tk
import requests

from core.speech_recognition import AuraSpeechRecognition
from core.config import Config
from core.db import init_db


def init_app():
    init_db(Config.db_file)

    root = tk.Tk()
    root.title('Aura')
    root.geometry('500x250')
    root.configure(background='black')

    try:
        requests.head("http://www.google.com/", timeout=Config.timeout)
    except requests.ConnectionError:
        # TODO: write these on screen and add text to speech
        print("The internet connection is down. Please reconnect and restart this app")

    # TODO: add a Aura server check. needs to be a paid user

    # TODO: check user. only allow one session per email

    # TODO: check for updates mechanism

    # Start the worker thread
    thread = threading.Thread(target=worker)
    thread.start()

    root.mainloop()

def worker():
   sr = AuraSpeechRecognition()
   sr.run()

if __name__ == '__main__':
    init_app()

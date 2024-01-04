import threading
import tkinter as tk
import requests
from selenium import webdriver

from core.speech_recognition import AuraSpeechRecognition
from core.config import Config
from core.db import init_db


def init_app():
    init_db(Config.db_file)

    root = tk.Tk()
    root.title('Aura')
    root.geometry('1000x250')

    aura_vocab_title = "Aura Vocab"
    aura_vocab_text = """
    Please ensure you have the latest version of Chrome downloaded. It should be located at 
    C:\Program Files\Google\Chrome\Application\chrome.exe. Aura will only work with Chrome.
    
    To do a search on your computer, say "search for Downloads on the computer"
    To search on Google, say "search for mountains on the web"
    To browse to a specific site, say "browse to google.com"
    To shop for something on amazon, say "Shop for underwears"
    """
    label = tk.Label(root, text=aura_vocab_text)
    label.pack()

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

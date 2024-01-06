import threading
import tkinter as tk
import requests
from selenium import webdriver

from core.speech_recognition import AuraSpeechRecognition
from core.config import Config
from core.db import init_db


# TODO: add fail case return statements
# TODO: speech recog tooooo slow. fasten it up

def init_app():
    init_db(Config.db_file)

    root = tk.Tk()
    root.title('Aura')
    root.geometry('1000x500')

    aura_vocab_title = "Aura Vocab"
    aura_vocab_text = """
    When Aura is ready, you will hear a notification sound.
    
    Say "Activate Voice" to begin giving commands to Aura.
    Say "Deactivate Voice" to deactivate Aura.
    
    To do a search on your computer, say "search for Downloads on the computer"
    To search for any folder on your system, say "Search for Downloads" or "Search for Test directory in D: drive"
    To search for a file mention where the file is, say "Search for untitled.txt in D drive in Test sub directory" 
    
    To search on Google, say "search for mountains on the web"
    To browse to a specific site, say "browse to google.com"
    To shop for something on amazon, say "Shop for headphones"
    To scroll down a page on chrome, say "Scroll down on Chrome"
    To open new tab or close current tab, say "Open new tab on the browser"
    To minimize or close browser window, say "Close browser window"
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
    # Create a new instance of the Firefox driver
    # TODO: only show when needed. not on startup
    driver = webdriver.Firefox()

    sr = AuraSpeechRecognition()
    sr.run(driver)

if __name__ == '__main__':
    init_app()

import os
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor

import requests
from selenium import webdriver
from selenium_stealth import stealth

from core.config import Config
from core.db import init_db
from core.speech_recognition import AuraSpeechRecognition


# TODO: add fail case return statements
# TODO: speech recog tooooo slow. fasten it up

def init_app():
    user_id = init_db(Config.db_file)

    root = tk.Tk()
    root.title('Aura')
    root.geometry('1000x500')

    aura_vocab_title = "Aura Vocab"
    aura_text = """
    When Aura is ready, you will hear a notification sound.
    
    Say "Activate Voice" to begin giving commands to Aura.
    Say "Deactivate Voice" to deactivate Aura.
    
    To do a search on your computer, say "search for Downloads on the computer"
    To search for any folder on your system, say "Search for Downloads" or "Search for Test directory in D: drive"
    To search for a file mention where the file is, say "Search for untitled.txt in D drive in Test sub directory"
    To find out what images are on the screen, say "What are the images on the screen right now?"
    To find out what is on the screen right now, say "Whats on the screen right now?"
    
    To search on Google, say "search for mountains on the web"
    To browse to a specific site, say "browse to google.com"
    To shop for something on amazon, say "Shop for headphones"
    To scroll down a page on chrome, say "Scroll down on Chrome"
    To open new tab or close current tab, say "Open new tab on the browser"
    To minimize or close browser window, say "Close browser window"
    To find out links on the page, say "What are the links on this webpage?"
    To click on a specific link like lets say an article from BuzzFeed, say "Link on the BuzzFeed link"  
    
    Pls Note: When the narration is going on, if a command is spoken, the narration will stop.
    """


    try:
        requests.head("http://www.google.com/", timeout=Config.timeout)
    except requests.ConnectionError:
        # TODO: write these on screen and add text to speech
        aura_text = "The internet connection is down. Please reconnect and restart this app"

    label = tk.Label(root, text=aura_text)
    label.pack()

    # TODO: add a Aura server check. needs to be a paid user

    # TODO: check user. only allow one session per email

    # TODO: check for updates mechanism

    # Create a new driver instance
    chrome_user_data = get_chrome_user_data_dir()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_user_data}")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get("https://www.google.com")

    # start all threads
    # worker_functions(driver, root)

    # Start the worker thread
    thread = threading.Thread(target=worker_speech_recognition, args=(driver,))
    thread.daemon = True
    thread.start()

    def on_close():
        driver.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()


def get_chrome_user_data_dir():
   """Returns the path to the Chrome user data directory."""
   if os.name == 'nt': # Windows
       return os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
   else:
       raise Exception("Unsupported operating system.")


# def worker_functions(driver, root):
#     with ThreadPoolExecutor(max_workers=1) as executor:
#         executor.submit(worker_speech_recognition, driver)
#
#         def on_close():
#             executor.shutdown(wait=False)
#             root.destroy()
#
#         root.protocol("WM_DELETE_WINDOW", on_close)


def worker_speech_recognition(driver):
    sr = AuraSpeechRecognition()
    sr.run(driver)


if __name__ == '__main__':
    init_app()

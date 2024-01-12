import threading
import tkinter as tk

import requests
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium_stealth import stealth

from aura.core.config import Config
from aura.core.db import init_db
from aura.core.driver_session import set_session_storage, save_session_storage, get_chrome_user_data_dir
from aura.core.speech_recognition import worker_speech_recognition


# TODO: add fail case return statements
# TODO: add else statements play_sound to inform user what is missing
# TODO: add a Aura server check. needs to be a paid user
# TODO: check user. only allow one session per email
# TODO: check for updates mechanism
# TODO: if there any active Chrome sessions, close them
# TODO write test for selenium element pick -> click_submit, email_actions


def init_app():
    user_id = init_db(Config.db_file)

    root = tk.Tk()
    root.title('Aura')
    root.geometry('1500x750')

    aura_title = "Welcome to Aura"
    title_label = tk.Label(root, text=aura_title, font=("Helvetica", 16))
    title_label.pack()

    aura_text = """
    When Aura is ready, you will hear a notification sound.
    
    Say "Activate" to begin giving commands to Aura.
    Say "Deactivate" to deactivate Aura.
    
    To do a search on your computer, say "search for Downloads on the computer"
    To search for any folder on your system, say "search for Program Files on the computer" or 
    "search for Test directory in D: drive"
    To search for a file mention where the file is, say "search for untitled.txt in D drive in 
    Test sub directory"
    To find out what images are on the screen, say "what are the images on the screen right now?"
    To find out what is on the screen right now, say "whats on the screen right now?"
    
    To search on Google, say "search for mountains on the web"
    To browse to a specific site, say "browse to google.com"
    To shop for something on amazon, say "shop for headphones"
    To scroll down a page on chrome, say "scroll down on Chrome"
    To open new tab or close current tab, say "open new tab on the browser"
    To minimize or close browser window, say "close/minimize browser window"
    To find out links on the page, say "what are the links on this webpage?"
    To click on a specific link like lets say an article from BuzzFeed, say "click on the BuzzFeed link"  
    To get a summary of the amazon product on the browser, say "please summarize the amazon product 
    on the page for me"
    To submit a form, say "Submit this form"
    To bookmark a page, say "Bookmark this page"
    To open a previously bookmarked page, say "Open the bookmark I have for BuzzFeed blog post about Keto diet" 
    To compose a Gmail message, say "Compose an email"
    To rewrite the mail you've composed, say "Touch up this email in a professional tone"  
    To open the attach files in mail, say "Attach a file to this email"
    To send an email, say "Send this email"
    If you have too much promotional junk and want to delete it all in one go, 
    just say "Delete all Promotional and Social mails"
    
    Pls Note: When the narration is going on, if a command is spoken, the narration will stop.

    Aura understands everything you say, the above are just examples. Please feel free to experiment and find out 
    how to make Aura work for you in the bext wat possible.
    """

    try:
        requests.head("http://www.google.com/", timeout=Config.timeout)
    except requests.ConnectionError:
        aura_text = "The internet connection is down. Please reconnect and restart this app"

    label = tk.Label(root, text=aura_text, justify="left")
    label.pack(padx=20, pady=20)

    # Create a new driver instance
    chrome_user_data = get_chrome_user_data_dir()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_user_data}")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0.4430.212 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')

    try:
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
    except SessionNotCreatedException:
        print("Chrome failed to start. Another session ongoing")

    def on_close():
        if driver:
            driver.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start the worker threads
    worker_speech_thread = threading.Thread(target=worker_speech_recognition, args=(driver,))
    worker_speech_thread.daemon = True
    worker_speech_thread.start()

    save_session_storage_thread = threading.Thread(target=save_session_storage, args=(driver,))
    save_session_storage_thread.daemon = True
    save_session_storage_thread.start()

    set_session_storage_thread = threading.Thread(target=set_session_storage, args=(driver,))
    set_session_storage_thread.daemon = True
    set_session_storage_thread.start()

    root.mainloop()

import threading
import time
import tkinter as tk
import requests
from selenium import webdriver

from core.speech_recognition import AuraSpeechRecognition
from core.config import Config
from core.db import init_db, load_cookies, add_cookies_to_db, check_cookie_exists


# TODO: add fail case return statements
# TODO: speech recog tooooo slow. fasten it up

def init_app():
    user_id = init_db(Config.db_file)

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

    # Create a new instance of the Firefox driver
    # TODO: only show when needed. not on startup
    driver = webdriver.Firefox()
    # load_cookies(driver=driver, user_id=user_id)

    # Start the worker thread
    # thread = threading.Thread(target=worker_speech_recognition, args=(driver,))
    # thread.start()

    # Start the worker thread
    thread = threading.Thread(target=worker_cookie, args=(driver, user_id))
    thread.start()

    root.mainloop()



def worker_speech_recognition(driver):
    sr = AuraSpeechRecognition()
    sr.run(driver)


def worker_cookie(driver, user_id):
   previous_cookies = []

   while True:
       cookie_script = """return document.cookie"""
       cookies = driver.execute_script(cookie_script)

       if cookies:
           current_url = """return window.location.hostname"""
           url = driver.execute_script(current_url)

            # TODO: fix the logic here
           # currently cookies getting stored individually.
           # find a way to check if most of the cookie string is similar, dont log it.
           # if cookie string not similar, then log it
           parsed_cookies = parse_cookies(cookies)
           print("parsed_cookies", parsed_cookies)

           for cookie_name, _ in parsed_cookies.items():
               print("cookie_name", cookie_name)

               is_cookie_exists = check_cookie_exists(user_id, url, cookie_name)
               print("is_cookie_exists", is_cookie_exists)

               if not is_cookie_exists:
                  print("adding cookie")
                  previous_cookies.append(cookie_name)
                  add_cookies_to_db(cookie_name, url, user_id)

       time.sleep(2)



def parse_cookies(cookies):
   cookie_dict = {}
   for cookie in cookies.split(';'):
       key, value = cookie.strip().split('=', 1)
       cookie_dict[key] = value
   return cookie_dict



if __name__ == '__main__':
    init_app()

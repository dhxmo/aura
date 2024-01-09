import time
import json
from urllib.parse import urlparse
import os


def get_chrome_user_data_dir():
   """Returns the path to the Chrome user data directory."""
   if os.name == 'nt': # Windows
       return os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
   else:
       raise Exception("Unsupported operating system.")


def save_session_storage(driver):
    current_dir = os.getcwd()
    session_storage_file_path = os.path.join(current_dir, 'session_storage.json')

    # Execute JavaScript code to save the session storage locally
    current_session_storage = driver.execute_script("return Object.assign({}, window.sessionStorage);")

    # Get the current hostname
    current_hostname = urlparse(driver.current_url).hostname

    try:
       # Try to load the session storage from the JSON file
       with open(session_storage_file_path, 'r') as f:
           session_storages = json.load(f)

       # Extract the session storage for the current hostname
       last_session_storage = session_storages.get(current_hostname)

       # Compare the current session storage with the last session storage
       if current_session_storage != last_session_storage:
           # Add the current session storage to the session storages
           session_storages[current_hostname] = current_session_storage

           # Write the session storages back to the JSON file
           with open(session_storage_file_path, 'w') as f:
               json.dump(session_storages, f)

    except FileNotFoundError:
       # If the JSON file does not exist, create it and write the current session storage to it
       with open(session_storage_file_path, 'w') as f:
           json.dump({current_hostname: current_session_storage}, f)

    # Pause the execution of the program for 5 seconds
    time.sleep(5)


def set_session_storage(driver):
    current_dir = os.getcwd()
    session_storage_file_path = os.path.join(current_dir, 'session_storage.json')

    # Get the current hostname
    current_hostname = urlparse(driver.current_url).hostname

    try:
        # Try to load the session storage from the JSON file
        with open(session_storage_file_path, 'r') as f:
            session_storages = json.load(f)

        # Extract the session storage for the current hostname
        session_storage = session_storages.get(current_hostname)

        if session_storage:
            # Execute JavaScript code to set the session storage
            for key, value in session_storage.items():
                driver.execute_script(f"window.sessionStorage.setItem('{key}', '{value}');")
    except FileNotFoundError:
        pass

    # Continuously check for new webpages
    while True:
        time.sleep(1)
        if driver.current_url != driver.execute_script("return window.location.href;"):
            # If a new webpage is visited, set the session storage
            set_session_storage(driver)
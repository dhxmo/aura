import threading

import dearpygui.dearpygui as dpg
import requests

from core.speech import SpeechRecognitionApp
from parser.db import init_db


def init_app():
    db_file = "aura.db"
    init_db(db_file)

    dpg.create_context()

    dpg.create_viewport(title='Aura', width=100, height=100)
    dpg.setup_dearpygui()

    # Check internet connection
    timeout = 1
    try:
        requests.head("http://www.google.com/", timeout=timeout)

        # TODO: add a Aura server check. needs to be a paid user

        # Create a thread for recognizing speech
        sr = SpeechRecognitionApp()
        speech_thread = threading.Thread(target=sr.run)
        speech_thread.start()

    except requests.ConnectionError:
        # Display error message in DearPyGUI viewport
        with dpg.window(label="Error"):
            dpg.add_text("The internet connection is down. Please reconnect and restart this app")

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    init_app()

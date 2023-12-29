import os
import threading

import dearpygui.dearpygui as dpg

from core.speech import SpeechRecognitionApp
from parser.db import create_user


def init_db():
    db_file = "aura.db"
    if not os.path.exists(db_file):
        with open(db_file, 'w'): pass

    is_user_create = create_user(db_file="aura.db")
    if is_user_create:
        return True


def init_app():
    check_db = init_db()

    if check_db:
        dpg.create_context()

        dpg.create_viewport(title='Aura', width=100, height=100)
        dpg.setup_dearpygui()

        # TODO: check internet connection. If no internet, give error. Else

        # TODO: check if update published. if yes, ask to update

        # Create a thread for recognizing speech
        sr = SpeechRecognitionApp()
        speech_thread = threading.Thread(target=sr.run)
        speech_thread.start()

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()


if __name__ == '__main__':
    init_app()

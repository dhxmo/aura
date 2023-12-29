import threading

import dearpygui.dearpygui as dpg

from core.speech import SpeechRecognitionApp


def init_app():
    dpg.create_context()

    dpg.create_viewport(title='Aura', width=100, height=100)
    dpg.setup_dearpygui()

    # Create a thread for recognizing speech
    sr = SpeechRecognitionApp()
    speech_thread = threading.Thread(target=sr.run)
    speech_thread.start()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    init_app()

import threading
import keyboard

from aura.core.utils import read_aloud, kill_engine



def worker_screen_reader(driver):
    while True:
        # Listen for 'TAB' key press event
        if keyboard.is_pressed('tab'):
            is_engine_killed = kill_engine()

            if is_engine_killed:
                current_title = None

                try:
                    # Get the current active element
                    active_element = driver.switch_to.active_element

                    try:
                        new_title = active_element.get_attribute('aria-label')
                        if new_title is None:
                            new_title = active_element.text
                    except Exception as e:
                        print("Error getting title: ", str(e))

                    if new_title != current_title:
                        current_title = new_title
                        # Start a new thread to run the speech
                        speech_thread = threading.Thread(target=read_aloud, args=(current_title,))
                        speech_thread.start()
                except Exception as e:
                    print("error in active_element {}".format(e))
import platform
import time

import pyautogui

from aura.core.utils import play_sound, read_aloud


def computer_search(detected_keyword):
    if platform.system() == "Windows":
        pyautogui.press("win")

        time.sleep(0.4)

        # Now type the text
        for char in detected_keyword:
            pyautogui.write(char)

        pyautogui.press("enter")

        read_aloud("Search complete for {}".format(detected_keyword))
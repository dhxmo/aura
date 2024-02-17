import platform
import time

import pyautogui

from aura.core.utils import play_sound


def computer_search(detected_keyword):
    if platform.system() == "Windows":
        pyautogui.press("win")

        time.sleep(0.4)

        # Now type the text
        for char in detected_keyword:
            pyautogui.write(char)

        pyautogui.press("enter")

        play_sound("Search complete for {}".format(detected_keyword))
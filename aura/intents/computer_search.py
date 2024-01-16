import platform
import time

import pyautogui


def computer_search(detected_keyword):
    if platform.system() == "Windows":
        pyautogui.press("win")

        time.sleep(0.4)

        # Now type the text
        for char in detected_keyword:
            pyautogui.write(char)

        pyautogui.press("enter")
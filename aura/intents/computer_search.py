import platform
import time

import pyautogui


def computer_search(detected_keyword):
    if platform.system() == "Windows":
        pyautogui.press("win")
    elif platform.system() == "Linux":
        pyautogui.press("win")
    else:
        # Press and release Command and Space separately
        pyautogui.keyDown("command")
        pyautogui.press("space")
        pyautogui.keyUp("command")

    time.sleep(1)

    # Now type the text
    for char in detected_keyword:
        pyautogui.write(char)

    pyautogui.press("enter")

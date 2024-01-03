import platform
import time

import pyautogui


def search(text):
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
    for char in text:
        pyautogui.write(char)

    pyautogui.press("enter")
    return "Open program: " + text

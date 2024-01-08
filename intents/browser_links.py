import base64
import os
import pyttsx3
import pyautogui

from core.utils import maximize_window_if_not_in_focus, take_rolling_screenshot
from engine.image_parse import format_vision_prompt, get_content_chat_completions


def summarize_links(driver):
    maximize_window_if_not_in_focus(driver)

    screenshot_file_path = take_rolling_screenshot(driver)

    # convert image to base64
    with open(screenshot_file_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # format vision prompt
        format_vision_prompt(user_objective="Summarize the links of this page")

        # send to openai vision
        res = get_content_chat_completions(img_base64=img_base64)

        # recite it out
        engine = pyttsx3.init()
        engine.say(res)
        engine.runAndWait()

        return
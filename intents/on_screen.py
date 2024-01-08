import base64
import os

import pyautogui
import pyttsx3

from engine.image_parse import format_vision_prompt, get_content_chat_completions


def on_screen(objective):
    if objective == 'images_on_screen':
        user_objective = """Talk about the image on this page. Describe only the images. Describe them in details 
        to someone who cannot see them. Be vivid in your descriptions"""
    elif objective == 'whats_on_screen':
        user_objective = "Talk about whats on the screen right now. Describe it in details."

    current_dir = os.getcwd()
    screenshot_file_path = os.path.join(current_dir, 'assets', 'screenshots', 'screenshot.png')

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    screenshot.save(screenshot_file_path)

    # convert image to base64
    with open(screenshot_file_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # format vision prompt
        format_vision_prompt(user_objective=user_objective)

        # send to openai vision
        res = get_content_chat_completions(img_base64=img_base64)

        # recite it out
        engine = pyttsx3.init()
        engine.say(res)
        engine.runAndWait()

        return
import base64
import io
import os
import re
import queue
import time

import pyttsx3
from PIL import Image
from playsound import playsound
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from aura.engine.image_parse import format_vision_prompt, get_content_chat_completions


def play_sound(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'aura', 'assets', 'audio', filename)
    playsound(file_path)
    return


# # Function to check if the WebDriver is in focus
# def is_driver_in_focus(driver):
#     # Save the initial active element
#     initial_active_element = driver.switch_to.active_element
#
#     return initial_active_element == driver.switch_to.active_element
#
#
# # Function to maximize the window if the WebDriver is not in focus
# def maximize_window_if_not_in_focus(driver):
#     if not is_driver_in_focus(driver):
#         driver.maximize_window()


def take_rolling_screenshot(driver, roll_down_steps, is_amazon=None):
    screenshot_file_path = get_screenshot_file()

    # Take screenshots and stitch them together
    screenshots = []

    # Get the current URL
    current_url = driver.current_url

    if is_amazon and 'https://www.amazon.com/' in current_url:
        # Take a screenshot of the product
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(Image.open(io.BytesIO(screenshot)))
        try:
            # go to customer reviews
            button = driver.find_element(By.ID, 'acrCustomerReviewLink')
            button.click()
        except NoSuchElementException:
            play_sound("No customer reviews were found on this page")
            return
    else:
        play_sound("Please open amazon.com to run this action")
        return

    for _ in range(roll_down_steps):
        # Take a screenshot
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(Image.open(io.BytesIO(screenshot)))

        # Scroll down the page
        driver.execute_script("window.scrollBy(0, 500)")

    # Stitch the screenshots together
    full_screenshot = Image.new('RGB', (screenshots[0].width, screenshots[0].height * len(screenshots)))
    for idx, screenshot in enumerate(screenshots):
        full_screenshot.paste(screenshot, (0, idx * screenshot.height))

    # Save the full screenshot
    full_screenshot.save(screenshot_file_path)

    return screenshot_file_path


def image_capture_n_parse(screenshot_file_path, user_objective):
    # convert image to base64
    with open(screenshot_file_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # format vision prompt
        vision_prompt = format_vision_prompt(user_objective=user_objective)

        # send to openai vision
        res = get_content_chat_completions(img_base64=img_base64, prompt=vision_prompt)

        # recite it out
        read_aloud(res)

        return

# def read_aloud(res):
#     print("running read aloud")
#     engine = pyttsx3.init()
#     # engine.setProperty('language', lang)
#     engine.say(res)
#     engine.runAndWait()
#     engine.stop()
#     return

engine = pyttsx3.init()

def read_aloud(res):
    # engine.setProperty('language', lang)
    engine.say(res)
    engine.runAndWait()
    engine.stop()

def kill_engine():
    global engine
    if engine is not None:
        engine.stop()
        return True


def get_screenshot_file():
    # take current screenshot
    current_dir = os.getcwd()
    screenshot_file_path = os.path.join(current_dir, 'aura', 'assets', 'screenshots', 'screenshot.png')

    # Check if the file exists
    if not os.path.isfile(screenshot_file_path):
        # If the file does not exist, create it
        open(screenshot_file_path, 'w').close()

    return screenshot_file_path


def clean_up_intent(intent):
    # Find the start and end indices of detected_keyword
    start = re.search('detected_keyword=\'', intent).end()
    end = intent.rfind("'", start)

    # Replace commas with spaces in detected_keyword
    detected_keyword = intent[start:end]
    detected_keyword = detected_keyword.replace(',', ' ')

    # Replace the original detected_keyword with the modified one
    intent = intent[:start] + detected_keyword + intent[end:]

    intent_list = intent.split(",")
    intent_dict = {elem.split("=")[0].strip(): elem.split("=")[1].strip("'") for elem in intent_list}

    return intent_dict
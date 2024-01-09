import base64
import os
import io

from playsound import playsound
from PIL import Image
import pyttsx3
from selenium.webdriver.common.by import By

from aura.engine.image_parse import format_vision_prompt, get_content_chat_completions


def play_sound(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'assets', 'audio', filename)
    playsound(file_path)

# Function to check if the WebDriver is in focus
def is_driver_in_focus(driver):
    # Save the initial active element
    initial_active_element = driver.switch_to.active_element

    return initial_active_element == driver.switch_to.active_element

# Function to maximize the window if the WebDriver is not in focus
def maximize_window_if_not_in_focus(driver):
   if not is_driver_in_focus(driver):
       driver.maximize_window()


def take_rolling_screenshot(driver, roll_down_steps, is_amazon=None):
    current_dir = os.getcwd()
    screenshot_file_path = os.path.join(current_dir, 'assets', 'screenshots', 'screenshot.png')

    # Take screenshots and stitch them together
    screenshots = []

    if is_amazon:
        # Take a screenshot of the product
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(Image.open(io.BytesIO(screenshot)))
        # go to customer reviews
        button = driver.find_element(By.ID, 'acrCustomerReviewLink')
        button.click()

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


def screenshot_2_voice(screenshot_file_path, user_objective):
    # convert image to base64
    with open(screenshot_file_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # format vision prompt
        format_vision_prompt(user_objective=user_objective)

        # send to openai vision
        res = get_content_chat_completions(img_base64=img_base64)

        # recite it out
        read_aloud(res)

def read_aloud(res):
    engine = pyttsx3.init()
    engine.say(res)
    engine.runAndWait()
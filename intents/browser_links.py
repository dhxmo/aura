import base64

import pyttsx3
from fuzzywuzzy import process
from selenium.webdriver.common.by import By

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

def click_link(driver, link_keyword):
    # Find all the links on the page
    links = driver.find_elements(By.TAG_NAME, 'a')

    # Create a dictionary to store the URLs and titles
    all_links = {}

    # Iterate over the links
    for link in links:
        # Get the link's href attribute (the URL) and the link's text (the title)
        url = link.get_attribute('href')
        title = link.text

        # Append the URL and title to the dictionary
        all_links[url] = title

    # Find the title that best matches the link keyword
    best_match = process.extractOne(link_keyword, all_links.values())

    # Click the link with the best match
    driver.get(next(key for key, value in all_links.items() if value == best_match[0]))

    return
import os

import pyautogui

from aura.core.utils import image_capture_n_parse, take_rolling_screenshot, get_screenshot_file


def on_screen(objective, driver=None):
    if objective == 'images_on_screen':
        user_objective = """Talk about the image on this page. Describe only the images. Describe them in details 
        to someone who cannot see them. Be vivid in your descriptions"""
    elif objective == 'whats_on_screen':
        user_objective = "Talk about whats on the screen right now. Describe it in details."
    elif objective == 'amazon_product_summary':
        user_objective = """Talk about the product on the page.
        Mention the following everytime: 
        1. name of the product
        2. what company/store the product is from
        3. what is the price,
        4. the average star rating on the product
        5. finally give a summary of the user reviews (are they positive/negative/neutral generally? 
        what are the average number of customer saying about this product?)"""
        screenshot_file_path = take_rolling_screenshot(driver=driver, roll_down_steps=4, is_amazon=True)
        image_capture_n_parse(screenshot_file_path=screenshot_file_path, user_objective=user_objective)
        return

    screenshot_file_path = get_screenshot_file()

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_file_path)

    image_capture_n_parse(screenshot_file_path=screenshot_file_path, user_objective=user_objective)
    return
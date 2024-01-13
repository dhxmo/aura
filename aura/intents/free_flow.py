import os
import re

import pyautogui

from aura.core.config import Config
from aura.core.utils import image_capture_n_parse, get_screenshot_file, clean_up_intent
from aura.engine.parser import parser

from aura.engine.runner import runner


def free_flow(user_action, driver):
    print("in free flow")

    # get screen width & height
    # screen_width, screen_height = pyautogui.size()
    #
    # screenshot_file_path = get_screenshot_file()
    #
    # screenshot = pyautogui.screenshot()
    # screenshot.save(screenshot_file_path)

    # Steps needed to take to achieve user goal
    # res_steps = image_capture_n_parse(screenshot_file_path=screenshot_file_path,
    #                       user_objective=user_action,
    #                       is_free_flow=True,
    #                       screen_width=screen_width,
    #                       screen_height=screen_height)
    res_steps = """1='Make sure Google Chrome is your active window',
    2='Click on the address bar at the top of the browser',
    3='Type "drive.google.com" and press Enter to navigate to Google Drive',
    4='Once in Google Drive, locate and click on the “New” button on the left side',
    5='In the drop-down menu, select “Google Docs”',
    6='Choose “Blank document” or a template if preferred'"""
    print("res", res_steps)

    # Split the string into pairs
    pairs = re.split(r'\d+=', res_steps)
    print("first pairs", pairs)

    # Iterate over each item in the list
    result = []
    for item in pairs:
        # Replace unwanted characters
        item = item.replace(",", "")
        item = item.replace("'", "")
        item = item.replace('"', "")
        item = item.replace("\\", "")

        # Split the string at each comma and add the parts to the result list
        parts = item.split(",")
        result.extend(parts)
    result = list(filter(None, result))

    # Initialize an empty dictionary
    intent_dict = {}
    # Add each element of the array as a key-value pair to the dictionary
    for i, item in enumerate(result, start=1):
        intent_dict[i] = item

    # Iterate over each step
    for key, value in intent_dict.items():
        print("key, value", key, value)

        intent = parser(payload=value, db_file=Config.db_file)
        print("intent", intent)
        #
        # f_intent_dict = clean_up_intent(intent)
        #
        # if f_intent_dict['command'] == 'free_flow':
        #     print("inside free flow")
        #     # format cursor_prompt
        #     # send screen height and width and map[step number] to get x,y position to click in
        #     # use pyautogui and click
        #     # take screenshot for current state
        #     # end loop
        # else:
        #     runner(f_intent_dict, driver)
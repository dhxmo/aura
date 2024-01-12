import os

import pyautogui

from aura.core.config import Config
from aura.core.utils import image_capture_n_parse, get_screenshot_file, clean_up_intent
from aura.engine.parser import parser

from aura.engine.runner import runner


def free_flow(user_action, driver):
    print("in free flow")

    # get screen width & height
    screen_width, screen_height = pyautogui.size()

    screenshot_file_path = get_screenshot_file()

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_file_path)

    # Steps needed to take to achieve user goal
    res_steps = image_capture_n_parse(screenshot_file_path=screenshot_file_path,
                          user_objective=user_action,
                          is_free_flow=True,
                          screen_width=screen_width,
                          screen_height=screen_height)
    # res_steps = """1='Open Google Chrome', 2='Navigate to https://drive.google.com/', 3='Click on the "+ New" button and select "Google Docs" to create a new document'"""
    print("res", res_steps)

    # Split the string into pairs
    pairs = res_steps.split(", ")

    # Convert each pair into a key-value pair and add it to the dictionary
    intent_dict = {}
    for pair in pairs:
        key, value = pair.split("=")
        intent_dict[key.strip()] = value.strip("'")
    print("intent_dict", intent_dict)
    # intent_dict = {
    #     1:'Open Google Chrome',
    #     2:'Navigate to https://drive.google.com/',
    #     3:'Click on the "+ New" button and select "Google Docs" to create a new document'
    # }

    # Iterate over each step
    for key, value in intent_dict.items():
        print("step", key, value)

        # intent = parser(payload=value, db_file=Config.db_file)
        # print("intent", intent)
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
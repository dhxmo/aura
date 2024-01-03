import base64
import json
import os
import re

from .screen_capture import capture_screenshot, get_last_assistant_message
from parser.action_parser import get_content_chat_completions, format_vision_prompt


def initiate_aura(user_objective):
    # messages history containing the user's objective
    assistant_message = {"role": "assistant",
                         "content": "Hello, I can help you with anything. What would you like done?"}
    user_message = {
        "role": "user",
        "content": f"Objective: {user_objective}",
    }
    messages = [assistant_message, user_message]
    print("messages", messages)

    # create screenshots dir
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    screenshot_filename = os.path.join(screenshots_dir, "screenshot.png")
    grid_screenshot_filename = os.path.join(screenshots_dir, "grid_screenshot.png")

    # capture current screen
    is_screenshot = capture_screenshot(screenshot_filename=screenshot_filename,
                                       grid_screenshot_filename=grid_screenshot_filename)

    if is_screenshot:
        # get last response from assistant
        previous_action = get_last_assistant_message(messages)

        with open(grid_screenshot_filename, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

            # add to prompt as the last action so there is reference of what needs to happen next
            vision_prompt = format_vision_prompt(user_objective=user_objective, previous_action=previous_action)
            content, messages = get_content_chat_completions(vision_prompt=vision_prompt,
                                                             img_base64=img_base64,
                                                             messages=messages)
            print("content", content)
            print("messages", messages)

            if content.startswith("CLICK"):
                click_data = re.search(r"CLICK \{ (.+) \}", content).group(1)
                click_data_json = json.loads(f"{{{click_data}}}")
                prev_x = click_data_json["x"]
                prev_y = click_data_json["y"]

                print("prev_x", prev_x)
                print("prev_y", prev_y)

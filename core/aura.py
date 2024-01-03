import base64
import os

from parser.action_parser import get_content_chat_completions, format_vision_prompt, parse_response
from .aura_actions import search, keyboard_type, mouse_click
from .screen_capture import capture_screenshot


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
            vision_prompt = format_vision_prompt(user_objective=user_objective,
                                                 previous_action=previous_action)

            print("vision_prompt", vision_prompt)

            content, messages = get_content_chat_completions(vision_prompt=vision_prompt,
                                                             img_base64=img_base64,
                                                             messages=messages)
            print("content", content)

            action = parse_response(content)
            print("action", action)

            action_type = action.get("type")
            action_detail = action.get("data")

            action_response = ''
            if action_type == "SEARCH":
                action_response = search(action_detail)
            elif action_type == "TYPE":
                action_response = keyboard_type(action_detail)
            elif action_type == "CLICK":
                action_response = mouse_click(action_detail)

            message = {
                "role": "assistant",
                "content": action_response,
            }
            messages = messages.append(message)

            print("messages", messages)


def get_last_assistant_message(messages):
    for index in reversed(range(len(messages))):
        if messages[index]["role"] == "assistant":
            if index == 0:  # Check if the assistant message is the first in the array
                return None
            else:
                return messages[index]
    return None  # Return None if no assistant message is found

import json
import logging
import re

from openai import OpenAI

from .config import Config

VISION_PROMPT = """
From looking at the screen and the objective your goal is to take action asked by the user in user_objective.

To operate the computer you have the four options below.

1. CLICK - Move mouse and click
2. TYPE - Type on the keyboard
3. SEARCH - Search for a program and open it
4. DONE - Job has been completed

Here are the response formats below.

1. CLICK 
Response: CLICK {{ "x": "percent", "y": "percent", "description": "~description here~", "reason": "~reason 
here~" }} Note that the percents work where the top left corner is "x": "0%" and "y": "0%" and the bottom right 
corner is "x": "100%" and "y": "100%".  

Aim to be highly accurate in this percentage. use the grid to determine the correct percentage where the element 
requested is located. Use the gris overlayed on top of the image to find the accurate position of elements on the 
screen. The percentage of where the element needs to be highly accurate. Calculate the total grid lines and then 
calculate where the element lies. finally output the percentage of x and y on the screen.

2. TYPE 
Response: TYPE "value you want to type"

3. SEARCH
Response: SEARCH "app you want to search for"

4. DONE
Response: DONE

Here are examples of how to respond. 
__ Objective: Open Spotify and play the beatles. SEARCH Spotify 

__ Objective: Find an image of a banana. CLICK {{ "x": "50%", "y": "60%", "description": "Click: Google Search field", "reason": "This 
will allow me to search for a banana" }} 

__ Objective: type amazon.com on the search bar. TYPE https://www.amazon.com/ __

A few important notes: 
- Go to Google Docs and Google Sheets by typing in the Chrome Address bar 

{previous_action}

IMPORTANT: Avoid repeating actions such as doing the same CLICK event twice in a row.

User Objective: {user_objective}
"""


def create_openai_client():
    client = OpenAI()
    client.api_key = Config.OPENAI_API_KEY
    return client


def get_content_chat_completions(vision_prompt, img_base64, messages):
    vision_message = {
        "role": "user",
        "content": [
            {"type": "text", "text": vision_prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
            },
        ],
    }

    # create a copy of messages and save to pseudo_messages
    pseudo_messages = messages.copy()
    pseudo_messages.append(vision_message)

    try:
        client = create_openai_client()
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=pseudo_messages,
            presence_penalty=1,
            frequency_penalty=1,
            temperature=0.7,
            max_tokens=300,
        )
        messages = messages.append(vision_message)

        return response.choices[0].message.content, messages
    except Exception as e:
        logging.info("Error occurred in get_content_chat_completions", str(e))
        return None


def format_vision_prompt(user_objective, previous_action):
    if previous_action:
        previous_action = f"Here was the previous action you took: {previous_action}"
    else:
        previous_action = ""
    return VISION_PROMPT.format(user_objective=user_objective, previous_action=previous_action)


def parse_response(response):
    print("response", response)
    try:
        if response == "DONE":
            return {"type": "DONE", "data": None}
        elif response.startswith("CLICK"):
            # Adjust the regex to match the correct format
            click_data = re.search(r"CLICK \{ (.+) \}", response).group(1)
            print("click_data", click_data)

            click_data_json = json.loads(f"{{{click_data}}}")
            print("click_data_json", click_data_json)

            return {"type": "CLICK", "data": click_data_json}

        elif response.startswith("TYPE"):
            type_data = re.search(r"TYPE (.+)", response, re.DOTALL).group(1)
            return {"type": "TYPE", "data": type_data}

        elif response.startswith("SEARCH"):
            # Extract the search query
            search_data = re.search(r'SEARCH "(.+)"', response).group(1)
            return {"type": "SEARCH", "data": search_data}

        return {"type": "UNKNOWN", "data": response}
    except Exception as e:
        logging.info(f"Error in parse_response: {e}")
        return None

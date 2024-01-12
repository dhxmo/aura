from openai import OpenAI

from aura.core.config import Config

VISION_PROMPT = """
User Objective: {user_objective}
It's important to say the following to help the user who's not able to see the screen understand whats on the screen right now.
From looking at the screen and based on the User Objective, report what you see on the screen.
"""

FREE_FLOW_PROMPT = """
The current screen's width and height is {screen_width} and {screen_height} respectively. I need to find out steps needed
to execute {user_action} from the current state given in the screenshot. 

If any steps require the following actions, please use these keywords in the step's description: web search, 
web browse,  web shop, navigate forward or back, summarize or click links, scroll up, down, top or bottom,
new or close tab, minimize or close window, find file or directory in explorer, find the images on screen, 
whats on screen, amazon product summary, submit form, save or open previous bookmark, compose, rewrite, attach file to 
or send email, delete promotional and social emails. If none of these actions are needed in the step, then explain the step 
as you must.

Keep response short and to the point. 
The output has to be in the format: "1='first step that would need to be taken to achieve user action',
 2='second step that would need to be taken', step3='third step that would need to be taken'"  
Stick to the above output format absolutely.
"""

COORDINATES_PROMPT = """"""

def create_openai_client():
    client = OpenAI()
    client.api_key = Config.OPENAI_API_KEY
    return client


def get_content_chat_completions(img_base64, prompt):
    vision_message = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
            },
        ],
    }]

    try:
        client = create_openai_client()
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=vision_message,
            presence_penalty=1,
            frequency_penalty=1,
            temperature=0.9,
            max_tokens=300,
        )

        return response.choices[0].message.content
    except Exception as e:
        print("Error occurred in get_content_chat_completions", str(e))
        return None


def format_vision_prompt(user_objective):
    return VISION_PROMPT.format(user_objective=user_objective)

def format_free_flow_prompt(screen_width, screen_height, user_action):
    return FREE_FLOW_PROMPT.format(screen_width=screen_width,
                                   screen_height=screen_height,
                                   user_action=user_action)
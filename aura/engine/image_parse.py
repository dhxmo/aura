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

If any steps require the following actions, please use these keywords in the step's description:
'web_search', 'web_browse', 'web_shop', 'navigate_forward', 'navigate_back', 'summarize_links', 'click_link', 
'scroll_up', 'scroll_down', 'scroll_top', 'scroll_bottom', 'new_tab', 'close_tab', 'minimize_window', 'close_window', 
'find_dir_in_explorer', 'find_file_in_dir', 'images_on_screen', 'whats_on_screen', 'amazon_product_summary', 
'submit_form', 'save_bookmark', 'open_previous_bookmark', 'compose_email', 'touch_up_email', 'attach_file_to_email',
'email_send', 'delete_promotional_n_socials'. If none of these actions are needed in the step, then explain the step 
as you must.

The output has to be in the format: "1='first step that would need to be taken to achieve user action',
 2='second step that would need to be taken', step3='third step that would need to be taken'"  
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
from openai import OpenAI

from core.config import Config

VISION_PROMPT = """
User Objective: {user_objective}
From looking at the screen and based on the User Objective, report what you see on the screen.
"""


def create_openai_client():
    client = OpenAI()
    client.api_key = Config.OPENAI_API_KEY
    return client


def get_content_chat_completions(img_base64):
    vision_message = [{
        "role": "user",
        "content": [
            {"type": "text", "text": VISION_PROMPT},
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
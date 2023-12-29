from openai import OpenAI

from .openai_api import OpenAIAPIClient, fetch_thread_msgs
from .config import Config
from .models import Assistant, db


def parser(payload):
    user_msg = payload["user_msg"]
    user_id = payload["user_id"]

    openai_client = OpenAIAPIClient(client=OpenAI(api_key=Config.OPENAI_API_KEY))

    # Query the Assistant table for any records
    user = Assistant.query.filter_by(user_id=user_id).first()

    if not user:
        new_user = Assistant(user_id=user_id)
        db.session.add(new_user)
        db.session.commit()

    # If a record exists, get the assistant_id from user record
    if user.assistant_id is not None:
        parser_assistant_id = user.assistant_id
        parser_thread_id = user.thread_id

        parser_run = openai_client.submit_message(assistant_id=parser_assistant_id,
                                                  thread_id=parser_thread_id,
                                                  user_message=user_msg)
    else:
        # create assistant
        parser_assistant_id = openai_client.get_assistant(Config.parser_custom_instruction).id
        parser_thread_id, parser_run = openai_client.create_thread_and_run(assistant_id=parser_assistant_id,
                                                                           user_input=user_msg)

        # Save the assistant ID in the database
        new_assistant = Assistant(assistant_id=parser_assistant_id, thread_id=parser_thread_id)
        db.session.add(new_assistant)
        db.session.commit()

    text = fetch_thread_msgs(openai_client=openai_client,
                             run=parser_run,
                             thread_id=parser_thread_id)
    return text
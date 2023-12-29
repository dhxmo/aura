import time


class OpenAIAPIClient:
    def __init__(self, client):
        self.client = client

    def get_all_messages_in_thread(self, thread_id):
        return self.client.beta.threads.messages.list(thread_id=thread_id, order="asc")

    def get_assistant(self, custom_instruction):
        parser_assistant = self.client.beta.assistants.create(
            name="browse-with-voice parser",
            instructions=custom_instruction,
            model="gpt-4-1106-preview"
        )

        return parser_assistant

    def submit_message(self, assistant_id, thread_id, user_message):
        self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_message
        )
        return self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

    def get_response(self, thread):
        return self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")

    def create_thread_and_run(self, assistant_id, user_input):
        thread = self.client.beta.threads.create()
        run = self.submit_message(assistant_id, thread.id, user_input)
        return thread.id, run

    # Waiting in a loop
    def wait_on_run(self, run, thread_id):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run


def fetch_thread_msgs(openai_client, run, thread_id):
    openai_client.wait_on_run(run, thread_id)
    res = openai_client.get_all_messages_in_thread(thread_id)

    assistant_msgs = []
    for message in res.data:
        if message.role == 'assistant':  # Check if the message is from the assistant
            if message.content[0].type == 'text':  # Check if the content is text
                text_value = message.content[0].text.value
                assistant_msgs.append(text_value)

    last_assistant_msg = assistant_msgs[-1] if assistant_msgs else None
    return last_assistant_msg
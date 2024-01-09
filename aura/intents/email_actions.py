import re

from selenium.webdriver.common.by import By
import sqlite3
from openai import OpenAI

from aura.core.config import Config
from aura.core.db import create_email_assistant_id
from aura.core.openai_api import OpenAIAPIClient, fetch_thread_msgs
from aura.core.utils import read_aloud
from aura.engine.parser import format_email_instruction
from aura.intents.browser_actions import driver_in_focus


def compose_email(driver):
    if driver:
        driver_in_focus(driver)

        # Get the current URL
        current_url = driver.current_url
        print("current url", current_url)

        # Check if the current URL is 'mail.google.com'
        if 'https://mail.google.com' in current_url:
           # Find the button with jsController="eIu7Db"
           button = driver.find_element(By.CSS_SELECTOR, 'div.T-I.T-I-KE.L3[jscontroller="eIu7Db"]')
           if button:
               # Click the button
               button.click()
               read_aloud("Cursor is on To. Type the email addresses you want to send the email to")
        return

def touch_up_email(driver, tone):
    if driver:
        driver_in_focus(driver)

        # Get the current URL
        current_url = driver.current_url
        print("current url", current_url)

        # Check if the current URL is 'mail.google.com'
        if 'https://mail.google.com' in current_url:
            # Find the element with the ID :64  ---> Message Body selector
            element = driver.find_element(By.CSS_SELECTOR, '#\\:64')
            text_content = element.get_property('textContent')

            email_instruction = format_email_instruction(message_body=text_content, email_tone=tone)
            new_email_content = email_assistant_client(payload=text_content, email_instruction=email_instruction)

            driver.execute_script("arguments[0].textContent = arguments[1];", element, new_email_content)

            read_aloud(f"Touched up email is as follows: {new_email_content}")


def email_assistant_client(payload, email_instruction):
    openai_client = OpenAIAPIClient(client=OpenAI(api_key=Config.OPENAI_API_KEY))

    try:
        conn = sqlite3.connect(Config.db_file)
        c = conn.cursor()

        # Fetch the first row from the table
        c.execute("SELECT * FROM assistants LIMIT 1")
        user = c.fetchone()

        if user:
            # user[4] - email_assistant_id
            # user[5] - email_thread_id
            if user[4] is not None and user[5] is not None:
                email_assistant_id = user[4]
                email_thread_id = user[5]

                email_run = openai_client.submit_message(assistant_id=email_assistant_id,
                                                          thread_id=email_thread_id,
                                                          user_message=payload)
            else:
                # create assistant
                email_assistant_id = openai_client.get_assistant(email_instruction).id
                email_thread_id, email_run = openai_client.create_thread_and_run(assistant_id=email_assistant_id,
                                                                                   user_input=payload)

                # user[1] - user_id
                create_email_assistant_id(user_id=user[1],
                                    assistant_id=email_assistant_id,
                                    thread_id=email_thread_id)

            text = fetch_thread_msgs(openai_client=openai_client,
                                     run=email_run,
                                     thread_id=email_thread_id)
            conn.close()

            return text
    except Exception as e:
        print("Error occurred while engine: ", str(e))
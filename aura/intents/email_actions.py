import re
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import sqlite3
from openai import OpenAI

from aura.core.config import Config
from aura.core.db import create_email_assistant_id
from aura.core.openai_api import OpenAIAPIClient, fetch_thread_msgs
from aura.core.utils import read_aloud
from aura.engine.parser import format_email_instruction
from aura.intents.browser_actions import driver_in_focus


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


def attach_file_to_email(driver):
    if driver:
        driver_in_focus(driver)
        file_input = driver.find_element(By.CSS_SELECTOR, '#\:6h')
        file_input.click()
        return

def email_send(driver):
    if driver:
        driver_in_focus(driver)
        send_btn = driver.find_element(By.CSS_SELECTOR, '#\:4k')
        send_btn.click()
        return

def delete_promotional_n_socials(driver):
    if driver:
        driver_in_focus(driver)

        promo_btn = driver.find_element(By.CSS_SELECTOR, '#\:1t')
        social_btn = driver.find_element(By.CSS_SELECTOR, '#\:1u')

        select_all_btn = driver.find_element(By.CSS_SELECTOR, '#\:1y > div.J-J5-Ji.J-JN-M-I-Jm > span')
        delete_btn = driver.find_element(By.CSS_SELECTOR, '#\:4 > div > div.nH.aqK > div.Cq.aqL > div > div > div:nth-child(2) > div.T-I.J-J5-Ji.nX.T-I-ax7.T-I-Js-Gs.mA > div')

        promo_btn.click()
        time.sleep(0.2)
        select_all_btn.click()
        time.sleep(0.3)
        try:
            # confirm google chrome browser css selector
            promo_select_all_btn = driver.find_element(By.CSS_SELECTOR, '#\:1m6')
            promo_select_all_btn.click()
        except NoSuchElementException:
            try:
                delete_btn.click()
            except ElementNotInteractableException:
                print("no mails to delete")
        time.sleep(1)

        social_btn.click()
        time.sleep(0.2)
        select_all_btn.click()
        time.sleep(0.3)
        try:
            # confirm google chrome browser css selector
            social_select_all_btn = driver.find_element(By.CSS_SELECTOR, '#\:wi')
            social_select_all_btn.click()
        except NoSuchElementException:
            try:
                delete_btn.click()
            except ElementNotInteractableException:
                print("no mails to delete")

        return
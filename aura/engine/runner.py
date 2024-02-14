from aura.core.utils import play_sound
from aura.intents.browser_actions import browser_actions, navigate, click_submit, open_bookmark
from aura.intents.browser_links import summarize_links, click_link
from aura.intents.clarify import clarify
from aura.intents.computer_explorer import find_dir_in_explorer, find_file_powershell
from aura.intents.computer_search import computer_search
from aura.intents.email_actions import compose_email, touch_up_email, attach_file_to_email, email_send
from aura.intents.on_screen import on_screen
# from aura.intents.pdf_read import read_the_pdf


def runner(intent_dict, driver):
    ready_sound = 'ready.mp3'

    match intent_dict['command']:
        case 'computer_search':
            computer_search(intent_dict['detected_keyword'])
        case 'web_search':
            browser_actions(driver=driver, detected_keyword=intent_dict['detected_keyword'], flag='web_search')
        case 'web_browse':
            browser_actions(driver=driver, detected_keyword=intent_dict['detected_keyword'], flag='web_browse')
        case 'web_shop':
            browser_actions(driver=driver, detected_keyword=intent_dict['detected_keyword'], flag='web_shop')
        case 'navigate_forward':
            navigate(driver=driver, navigation_type='forward')
        case 'navigate_back':
            navigate(driver=driver, navigation_type='back')
        # case 'find_dir_in_explorer':
        #     if intent_dict['root_directory'] == '':
        #         intent_dict['root_directory'] = None
        #     find_dir_in_explorer(directory=intent_dict['detected_keyword'], drive=intent_dict['root_directory'])
        # case 'find_file_in_dir':
        #     if intent_dict['root_directory'] == '':
        #         intent_dict['root_directory'] = None
        #     find_file_powershell(name=intent_dict['detected_keyword'], directory=intent_dict['root_directory'])
        case 'summarize_links':
            summarize_links(driver=driver)
        case 'click_link':
            click_link(driver=driver, link_keyword=intent_dict['detected_keyword'])
        case 'images_on_screen':
            on_screen(objective='images_on_screen')
        case 'whats_on_screen':
            on_screen(objective='whats_on_screen')
        case 'amazon_product_summary':
            on_screen(objective='amazon_product_summary', driver=driver)
        case 'submit_form':
            click_submit(driver)
        case 'open_bookmark':
            open_bookmark(driver=driver, keyword=intent_dict['detected_keyword'])
        case 'compose_email':
            compose_email(driver)
        case 'touch_up_email':
            touch_up_email(driver=driver, tone=intent_dict['detected_keyword'])
        case 'attach_file_to_email':
            attach_file_to_email(driver=driver)
        case 'email_send':
            email_send(driver)
        # case 'read_the_pdf':
        #     read_the_pdf()
        case 'clarify':
            clarify()

    play_sound(ready_sound)
    return

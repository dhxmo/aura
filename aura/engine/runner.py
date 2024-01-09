from aura.core.utils import play_sound
from aura.intents.browser_actions import browser_actions, navigate, scroll, window, tab, click_submit, save_bookmark, \
    open_bookmark
from aura.intents.browser_links import summarize_links, click_link
from aura.intents.clarify import clarify
from aura.intents.computer_explorer import find_dir_in_explorer, find_file_powershell
from aura.intents.computer_search import computer_search
from aura.intents.on_screen import on_screen


def runner(intent, driver):
    ready_sound = 'ready.mp3'

    intent_list = intent.split(",")
    intent_dict = {elem.split("=")[0].strip():elem.split("=")[1].strip("'") for elem in intent_list}

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
        case 'scroll_up':
            scroll(driver=driver, scroll_type='up')
        case 'scroll_down':
            scroll(driver=driver, scroll_type='down')
        case 'scroll_top':
            scroll(driver=driver, scroll_type='top')
        case 'scroll_bottom':
            scroll(driver=driver, scroll_type='bottom')
        case 'new_tab':
            tab(driver=driver, action_type='new')
        case 'close_tab':
            tab(driver=driver, action_type='close')
        case 'minimize_window':
            window(driver=driver, action_type='minimize')
        case 'close_window':
            window(driver=driver, action_type='close')
        case 'find_dir_in_explorer':
            if intent_dict['root_directory'] == '':
                intent_dict['root_directory'] = None
            find_dir_in_explorer(directory=intent_dict['detected_keyword'], drive=intent_dict['root_directory'])
        case 'find_file_in_dir':
            if intent_dict['root_directory'] == '':
                intent_dict['root_directory'] = None
            find_file_powershell(name=intent_dict['detected_keyword'], directory=intent_dict['root_directory'])
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
        case 'save_bookmark':
            save_bookmark(driver)
        case 'open_bookmark':
            open_bookmark(driver=driver, keyword=intent_dict['detected_keyword'])
        case 'clarify':
            clarify()

    play_sound(ready_sound)
    return
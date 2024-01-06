from intents.browser_actions import browser_actions, navigate, scroll, window, tab
from intents.computer_search import computer_search
from intents.find_in_explorer import find_dir_in_explorer, find_file_powershell


def runner(intent, driver):
    print("intent", intent)

    intent_list = intent.split(",")
    intent_dict = {elem.split("=")[0].strip():elem.split("=")[1].strip("'") for elem in intent_list}

    match intent_dict['command']:
        case 'computer_search':
            computer_search(intent_dict['detected_keyword'])
            return
        case 'web_search':
            browser_actions(driver=driver, detected_keyword=intent_dict['detected_keyword'], flag='web_search')
            return
        case 'web_browse':
            browser_actions(driver=driver, detected_keyword=intent_dict['detected_keyword'], flag='web_browse')
            return
        case 'web_shop':
            browser_actions(driver=driver, detected_keyword=intent_dict['detected_keyword'], flag='web_shop')
            return
        case 'navigate_forward':
            navigate(driver=driver, navigation_type='forward')
            return
        case 'navigate_back':
            navigate(driver=driver, navigation_type='back')
            return
        case 'scroll_up':
            scroll(driver=driver, scroll_type='up')
            return
        case 'scroll_down':
            scroll(driver=driver, scroll_type='down')
            return
        case 'scroll_top':
            scroll(driver=driver, scroll_type='top')
            return
        case 'scroll_bottom':
            scroll(driver=driver, scroll_type='bottom')
            return
        case 'new_tab':
            tab(driver=driver, action_type='new')
            return
        case 'close_tab':
            tab(driver=driver, action_type='close')
            return
        case 'minimize_window':
            window(driver=driver, action_type='minimize')
            return
        case 'close_window':
            window(driver=driver, action_type='close')
            return
        case 'find_dir_in_explorer':
            if intent_dict['root_directory'] == '':
                intent_dict['root_directory'] = None
            find_dir_in_explorer(directory=intent_dict['detected_keyword'], drive=intent_dict['root_directory'])
            return
        case 'find_file_in_dir':
            if intent_dict['root_directory'] == '':
                intent_dict['root_directory'] = None
            find_file_powershell(name=intent_dict['detected_keyword'], directory=intent_dict['root_directory'])

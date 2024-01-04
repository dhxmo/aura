from intents.browser_actions import browser_actions, navigate, scroll, window, tab
from intents.computer_search import computer_search

def runner(intent):
    print("intent", intent)

    intent_list = intent.split(",")
    intent_dict = {elem.split("=")[0].strip():elem.split("=")[1].strip("'") for elem in intent_list}

    match intent_dict['command']:
        case 'computer_search':
            computer_search(intent_dict['detected_keyword'])
            return
        case 'web_search':
            browser_actions(detected_keyword=intent_dict['detected_keyword'], flag='web_search')
            return
        case 'web_browse':
            browser_actions(detected_keyword=intent_dict['detected_keyword'], flag='web_browse')
            return
        case 'web_shop':
            browser_actions(detected_keyword=intent_dict['detected_keyword'], flag='web_shop')
            return
        case 'navigate_forward':
            navigate(navigation_type='forward')
            return
        case 'navigate_back':
            navigate(navigation_type='back')
            return
        case 'scroll_up':
            scroll(scroll_type='up')
            return
        case 'scroll_down':
            scroll(scroll_type='down')
            return
        case 'new_tab':
            tab(action_type='new')
            return
        case 'close_tab':
            tab(action_type='close')
            return
        case 'minimize_window':
            window(action_type='minimize')
            return
        case 'close_window':
            window(action_type='close')
            return
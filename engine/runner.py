from intents.browser_actions import browser_actions, navigate
from intents.computer_search import computer_search

def runner(intent):
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


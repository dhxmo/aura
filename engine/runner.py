from intents.computer_search import computer_search
from intents.web_browse import web_browse
from intents.web_search import web_search
from intents.web_shop import web_shop


def runner(intent):
    print("intent", intent)

    intent_list = intent.split(",")
    intent_dict = {elem.split("=")[0].strip():elem.split("=")[1].strip("'") for elem in intent_list}

    match intent_dict['command']:
        case 'computer_search':
            computer_search(intent_dict['detected_keyword'])
            return
        case 'web_search':
            web_search(intent_dict['detected_keyword'])
            return
        case 'web_browse':
            web_browse(intent_dict['detected_keyword'])
            return
        case 'web_shop':
            web_shop(intent_dict['detected_keyword'])
            return
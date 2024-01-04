from intents.search import search


def runner(intent):
    intent_list = intent.split(",")
    intent_dict = {elem.split("=")[0].strip():elem.split("=")[1].strip("'") for elem in intent_list}

    match intent_dict['command']:
        case 'search':
            search(intent_dict['detected_keyword'])
            return
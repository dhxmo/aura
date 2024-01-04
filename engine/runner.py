from intents.computer_search import computer_search

def runner(driver, intent):
    intent_list = intent.split(",")
    intent_dict = {elem.split("=")[0].strip():elem.split("=")[1].strip("'") for elem in intent_list}

    match intent_dict['command']:
        case 'computer_search':
            computer_search(intent_dict['detected_keyword'])
            return
        case 'web_search':
            url = f"https://www.google.com/search?q={intent_dict['detected_keyword']}"
            driver.get(url)
            return
        case 'web_browse':
            driver.get(intent_dict['detected_keyword'])
            return
        case 'web_shop':
            url = f"https://www.amazon.com/s?k={intent_dict['detected_keyword']}"
            driver.get(url)
            return
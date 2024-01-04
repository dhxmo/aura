import webbrowser


def browser_actions(detected_keyword, flag):
    if flag=='web_search':
        url = f"https://www.google.com/search?q={detected_keyword}"
    elif flag=='web_browse':
        url = detected_keyword
    elif flag=='web_shop':
        url = f"https://www.amazon.com/s?k={'detected_keyword'}"

    webbrowser.open_new(url)
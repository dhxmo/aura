import webbrowser

def web_search(detected_keyword):
    url = f"https://www.google.com/search?q={detected_keyword}"
    webbrowser.open(url)
    return
import webbrowser

def web_shop(detected_keyword):
    url = f"https://www.amazon.com/s?k={detected_keyword}"
    webbrowser.open(url)
    return
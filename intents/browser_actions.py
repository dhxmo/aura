import os
import webbrowser
import pyautogui

def browser_actions(detected_keyword, flag):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

    if flag=='web_search':
        url = f"https://www.google.com/search?q={detected_keyword}"
    elif flag=='web_browse':
        url = detected_keyword
    elif flag=='web_shop':
        url = f"https://www.amazon.com/s?k={'detected_keyword'}"

    webbrowser.get('chrome').open_new_tab(url)

def navigate(navigation_type):
    current_dir = os.getcwd()

    if navigation_type=='back':
        button_screenshot = os.path.join(current_dir, 'assets', 'chrome', 'chrome-back.png')
    elif navigation_type=='forward':
        button_screenshot = os.path.join(current_dir, 'assets', 'chrome', 'chrome-forward.png')

    # Locate the screenshot of the back button on the screen
    location = pyautogui.locateOnScreen(button_screenshot)

    if location is not None:
        # Click the center of the located region
        pyautogui.click(location[0] + location[2] // 2, location[1] + location[3] // 2)
    else:
        print("Back button not found.")
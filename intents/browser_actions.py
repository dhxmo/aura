import os
import time
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

    location = pyautogui.locateOnScreen(button_screenshot)

    if location is not None:
        # Click the center of the located region
        pyautogui.click(location[0] + location[2] // 2, location[1] + location[3] // 2)
    else:
        print("Button not found.")

def scroll(scroll_type):
    current_dir = os.getcwd()

    if scroll_type == 'up':
        button_screenshot = os.path.join(current_dir, 'assets', 'chrome', 'scroll-up.png')
    elif scroll_type == 'down':
        button_screenshot = os.path.join(current_dir, 'assets', 'chrome', 'scroll-down.png')

    location = pyautogui.locateOnScreen(button_screenshot)

    if location is not None:
        # Move the mouse to the center of the located region
        pyautogui.moveTo(location[0] + location[2] // 2, location[1] + location[3] // 2)

        # Press the mouse button down
        pyautogui.mouseDown()

        # Wait for a while (simulate a long press)
        time.sleep(1)

        # Release the mouse button
        pyautogui.mouseUp()
    else:
        print("Button not found.")

def tab(action_type):
    current_dir = os.getcwd()

    if action_type == 'new':
        button_screenshot = os.path.join(current_dir, 'assets', 'chrome', 'tab-new.png')
    elif action_type == 'close':
        button_screenshot = os.path.join(current_dir, 'assets', 'chrome', 'tab-close.png')

    location = pyautogui.locateOnScreen(button_screenshot)

    if location is not None:
        # Click the center of the located region
        pyautogui.click(location[0] + location[2] // 2, location[1] + location[3] // 2)
    else:
        print("Button not found.")

def window(action_type):
    current_dir = os.getcwd()

    if action_type == 'minimize':
        button_screenshot = os.path.join(current_dir, 'assets', 'chrome', 'window-minimize.png')
    elif action_type == 'close':
        button_screenshot = os.path.join(current_dir, 'assets', 'chrome', 'window-close.png')

    location = pyautogui.locateOnScreen(button_screenshot)

    if location is not None:
        # Click the center of the located region
        pyautogui.click(location[0] + location[2] // 2, location[1] + location[3] // 2)
    else:
        print("Button not found.")
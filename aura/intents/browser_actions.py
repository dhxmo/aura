import time

import pyautogui
import pygetwindow as gw
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException
from selenium.webdriver.common.by import By

from aura.core.utils import read_aloud, read_aloud


def browser_actions(driver, detected_keyword, flag):
    driver_in_focus(driver)

    if flag == 'web_search':
        url = f"https://www.google.com/search?q={detected_keyword}"
        play_res = "Web search complete for {}".format(detected_keyword)
    elif flag == 'web_browse':
        url = detected_keyword
        play_res = "Web browse complete for {}".format(detected_keyword)
    elif flag == 'web_shop':
        url = f"https://www.amazon.com/s?k={detected_keyword}"
        play_res = "Amazon search for {} complete".format(detected_keyword)

    driver.get(url)
    read_aloud(play_res)
    return


def window(driver, action_type):
    if driver:
        # Get the current window handle
        current_handle = driver.current_window_handle

        # Get a list of all window handles
        all_handles = driver.window_handles

        if action_type == 'minimize':
            # Check if the current window handle is in the list of all window handles
            if current_handle in all_handles:
                driver.minimize_window()
            else:
                print("Window does not exist.")
        elif action_type == 'maximize':
            # Check if the current window handle is in the list of all window handles
            if current_handle in all_handles:
                driver.maximize_window()
            else:
                print("Window does not exist.")
        elif action_type == 'close':
            if current_handle in all_handles:
                driver.quit()
            else:
                print("Window does not exist.")

        return
    else:
        read_aloud("Error in driver. Please restart the app.")
        return

def driver_in_focus(driver):
    try:
        window(driver=driver, action_type='maximize')

        # Get the title of the current window
        current_window_title = driver.title

        # Get the currently active window
        active_window = gw.getActiveWindow()

        # Get the window with the current title
        windows = gw.getWindowsWithTitle(current_window_title)

        if windows:
            current_window = windows[0]

            if active_window != current_window:
                current_window.activate()

        time.sleep(0.2)
        return
    except gw.PyGetWindowException:
        read_aloud("There was an error. Please restart the app.")


def navigate(driver, navigation_type):
    if driver:
        driver_in_focus(driver)

        if navigation_type == 'back':
            driver.back()
            read_aloud("Navigate back complete")
        elif navigation_type == 'forward':
            driver.forward()
            read_aloud("Navigate forward complete")

        return
    else:
        read_aloud("Error in driver. Please restart the app.")
        return


def click_submit(driver):
    if driver:
        driver_in_focus(driver)
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
            button.click()
            read_aloud("Submit button click complete")
        except NoSuchElementException:
            read_aloud("No submit button was found on the current page")

        return
    else:
        read_aloud("Error in driver. Please restart the app.")
        return


def open_bookmark(driver, keyword):
    if driver:
        driver_in_focus(driver)

        # Navigate to the bookmarks page
        driver.get('chrome://bookmarks')

        time.sleep(0.7)

        # Press Tab four times to get to search bar
        pyautogui.press('tab', presses=2, interval=0.1)

        # Type the keyword into the search bar
        pyautogui.write(keyword, interval=0.1)

        time.sleep(0.3)

        # Press Tab four times to get to the top bookmark
        pyautogui.press('tab', presses=4, interval=0.1)

        time.sleep(0.2)

        # Press Enter to submit the form
        pyautogui.press('space')
        pyautogui.press('enter')

        read_aloud("Open bookmark {} complete".format(keyword))

        return
    else:
        read_aloud("Error in driver. Please restart the app.")
        return



# def scroll(driver, scroll_type):
#     if driver:
#         driver_in_focus(driver)
#
#         try:
#             if scroll_type == 'up':
#                 driver.execute_script("window.scrollBy(0, -250)")
#             elif scroll_type == 'down':
#                 driver.execute_script("window.scrollBy(0, 250)")
#             elif scroll_type == 'top':
#                 driver.execute_script("window.scrollTo(0, 0)")
#             elif scroll_type == 'bottom':
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#         except NoSuchWindowException:
#             print("Window is no longer available.")
#
#         return
#     else:
#         read_aloud("Error in driver. Please restart the app.")
#         return
#
# def tab(driver, action_type):
#     if driver:
#         driver_in_focus(driver)
#
#         if action_type == 'new':
#             driver.execute_script("window.open('');")
#
#             # Get a list of all window handles
#             all_handles = driver.window_handles
#
#             # Switch to the last handle (which should be the new tab)
#             driver.switch_to.window(all_handles[-1])
#         elif action_type == 'close':
#             driver.execute_script("window.close();")
#
#         return
#
#
# def save_bookmark(driver):
#     if driver:
#         driver_in_focus(driver)
#
#         # Press Ctrl + D to bookmark the page
#         pyautogui.hotkey('ctrl', 'd')
#
#         time.sleep(0.4)
#
#         # Press Enter to confirm the bookmark
#         pyautogui.press('enter')
#
#         return
#     else:
#         read_aloud("Error in driver. Please restart the app.")
#         return
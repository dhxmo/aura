import time

import pyautogui
import pygetwindow as gw
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException
from selenium.webdriver.common.by import By


def browser_actions(driver, detected_keyword, flag):
    if flag == 'web_search':
        url = f"https://www.google.com/search?q={detected_keyword}"
    elif flag == 'web_browse':
        url = detected_keyword
    elif flag == 'web_shop':
        url = f"https://www.amazon.com/s?k={detected_keyword}"

    driver.get(url)


def navigate(driver, navigation_type):
    if driver:
        driver_in_focus(driver)

        if navigation_type == 'back':
            driver.back()
        elif navigation_type == 'forward':
            driver.forward()

        return


def scroll(driver, scroll_type):
    if driver:
        driver_in_focus(driver)

        try:
            if scroll_type == 'up':
                driver.execute_script("window.scrollBy(0, -250)")
            elif scroll_type == 'down':
                driver.execute_script("window.scrollBy(0, 250)")
            elif scroll_type == 'top':
                driver.execute_script("window.scrollTo(0, 0)")
            elif scroll_type == 'bottom':
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        except NoSuchWindowException:
            print("Window is no longer available.")

        return


def tab(driver, action_type):
    if driver:
        driver_in_focus(driver)

        if action_type == 'new':
            driver.execute_script("window.open('');")

            # Get a list of all window handles
            all_handles = driver.window_handles

            # Switch to the last handle (which should be the new tab)
            driver.switch_to.window(all_handles[-1])
        elif action_type == 'close':
            driver.execute_script("window.close();")

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


def click_submit(driver):
    if driver:
        driver_in_focus(driver)
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
            button.click()
        except NoSuchElementException:
            print("no such element found")
        return


def save_bookmark(driver):
    if driver:
        driver_in_focus(driver)

        # Press Ctrl + D to bookmark the page
        pyautogui.hotkey('ctrl', 'd')

        time.sleep(0.4)

        # Press Enter to confirm the bookmark
        pyautogui.press('enter')

        return


def open_bookmark(driver, keyword):
    if driver:
        driver_in_focus(driver)

        # Navigate to the bookmarks page
        driver.get('chrome://bookmarks')

        try:
            time.sleep(1)

            # Press Tab four times
            pyautogui.press('tab', presses=2, interval=0.1)

            # Type the keyword into the search bar
            pyautogui.write(keyword, interval=0.1)

            time.sleep(1)

            # Press Tab four times
            pyautogui.press('tab', presses=4, interval=0.1)

            time.sleep(1)

            # Press Enter to submit the form
            pyautogui.press('space')
            pyautogui.press('enter')

        except NoSuchElementException:
            print("No such element found")


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

            # If the currently active window is not the window with the current title, activate it
            if active_window != current_window:
                current_window.activate()

        time.sleep(1)
    except gw.PyGetWindowException:
        print("error code: 0 - Operation completed successfully")

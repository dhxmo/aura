from selenium.webdriver.common.by import By


def browser_actions(driver, detected_keyword, flag):
    if flag=='web_search':
        url = f"https://www.google.com/search?q={detected_keyword}"
    elif flag=='web_browse':
        url = detected_keyword
    elif flag=='web_shop':
        url = f"https://www.amazon.com/s?k={detected_keyword}"

    driver.get(url)


def navigate(driver, navigation_type):
    if navigation_type == 'back':
        driver.back()
    elif navigation_type=='forward':
        driver.forward()

def scroll(driver, scroll_type):
    if scroll_type == 'up':
        driver.execute_script("window.scrollBy(0, -250)")
    elif scroll_type == 'down':
        driver.execute_script("window.scrollBy(0, 250)")
    elif scroll_type == 'top':
        driver.execute_script("window.scrollTo(0, 0)")
    elif scroll_type == 'bottom':
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    return

def tab(driver, action_type):
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
    if action_type == 'minimize':
       # Get the current window handle
       current_handle = driver.current_window_handle

       # Get a list of all window handles
       all_handles = driver.window_handles

       # Check if the current window handle is in the list of all window handles
       if current_handle in all_handles:
           driver.minimize_window()
       else:
           print("Window does not exist.")
    elif action_type == 'close':
       current_handle = driver.current_window_handle
       all_handles = driver.window_handles
       if current_handle in all_handles:
           driver.quit()
       else:
           print("Window does not exist.")

    return

def click_submit(driver):
    button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    button.click()
    return
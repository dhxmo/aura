from fuzzywuzzy import process
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from aura.core.utils import maximize_window_if_not_in_focus, take_rolling_screenshot, image_capture_n_parse, play_sound
from aura.intents.browser_actions import driver_in_focus


def summarize_links(driver):
    driver_in_focus(driver)
    screenshot_file_path = take_rolling_screenshot(driver=driver, roll_down_steps=4)
    image_capture_n_parse(screenshot_file_path=screenshot_file_path, user_objective="Summarize the links of this page")
    return


def click_link(driver, link_keyword):
    try:
        # Find all the links on the page
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Create a dictionary to store the URLs and titles
        all_links = {}

        # Iterate over the links
        for link in links:
            # Get the link's href attribute (the URL) and the link's text (the title)
            url = link.get_attribute('href')
            title = link.text

            if url and title:
                # Append the URL and title to the dictionary
                all_links[url] = title

        # Find the title that best matches the link keyword
        best_match = process.extractOne(link_keyword, all_links.values())

        # Click the link with the best match
        driver.get(next(key for key, value in all_links.items() if value == best_match[0]))

        return
    except NoSuchElementException:
        play_sound("No hyperlinks were found on this page")
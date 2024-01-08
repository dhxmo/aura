import os
from playsound import playsound
from PIL import Image
import io


def play_sound(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'assets', 'audio', filename)
    playsound(file_path)

# Function to check if the WebDriver is in focus
def is_driver_in_focus(driver):
    # Save the initial active element
    initial_active_element = driver.switch_to.active_element

    return initial_active_element == driver.switch_to.active_element

# Function to maximize the window if the WebDriver is not in focus
def maximize_window_if_not_in_focus(driver):
   if not is_driver_in_focus(driver):
       driver.maximize_window()


def take_rolling_screenshot(driver):
    current_dir = os.getcwd()
    screenshot_file_path = os.path.join(current_dir, 'assets', 'screenshots', 'screenshot.png')

    # Take screenshots and stitch them together
    screenshots = []
    for _ in range(4):
        # Scroll down the page
        driver.execute_script("window.scrollBy(0, 500)")

        # Take a screenshot
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(Image.open(io.BytesIO(screenshot)))

    # Stitch the screenshots together
    full_screenshot = Image.new('RGB', (screenshots[0].width, screenshots[0].height * len(screenshots)))
    for idx, screenshot in enumerate(screenshots):
        full_screenshot.paste(screenshot, (0, idx * screenshot.height))

    # Save the full screenshot
    full_screenshot.save(screenshot_file_path)

    return screenshot_file_path
import pyautogui
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor


def capture_screenshot(screenshot_filename, grid_screenshot_filename):
    # Capture the screenshot of the current window
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    screenshot.save(screenshot_filename)

    # create new image with grid overlay
    add_grid_to_image(screenshot_filename, grid_screenshot_filename, grid_interval=7)

    return True


def add_grid_to_image(original_image_path, new_image_path, grid_interval):
    # Load the image
    image = Image.open(original_image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Get the image size
    width, height = image.size

    # Use a ThreadPoolExecutor to draw the vertical and horizontal lines in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(draw_vertical_lines, draw, width, height, grid_interval)
        executor.submit(draw_horizontal_lines, draw, width, height, grid_interval)

    # Save the image with the grid
    image.save(new_image_path)


def draw_vertical_lines(draw, width, height, interval):
    for x in range(interval, width, interval):
        line = ((x, 0), (x, height))
        draw.line(line, fill="blue")


def draw_horizontal_lines(draw, width, height, interval):
    for y in range(interval, height, interval):
        line = ((0, y), (width, y))
        draw.line(line, fill="blue")


def get_last_assistant_message(messages):
    for index in reversed(range(len(messages))):
        if messages[index]["role"] == "assistant":
            if index == 0:  # Check if the assistant message is the first in the array
                return None
            else:
                return messages[index]
    return None  # Return None if no assistant message is found

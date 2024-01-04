# import pyautogui
# from PIL import Image, ImageDraw
#
#
# def capture_screenshot(screenshot_filename, grid_screenshot_filename):
#     # Capture the screenshot of the current window
#     screenshot = pyautogui.screenshot()
#
#     # Save the screenshot to a file
#     screenshot.save(screenshot_filename)
#
#     # create new image with grid overlay
#     add_grid_to_image(screenshot_filename, grid_screenshot_filename, grid_interval=30)
#
#     return True
#
#
# def add_grid_to_image(original_image_path, new_image_path, grid_interval):
#     # Load the image
#     image = Image.open(original_image_path)
#
#     # Create a drawing object
#     draw = ImageDraw.Draw(image)
#
#     # Get the image size
#     width, height = image.size
#
#     # Reduce the font size a bit
#     font_size = int(grid_interval / 5)  # Reduced font size
#
#     # Calculate the background size based on the font size
#     bg_width = int(font_size * 4.2)  # Adjust as necessary
#     bg_height = int(font_size * 1.2)  # Adjust as necessary
#
#     # Function to draw text with a white rectangle background
#     def draw_label_with_background(
#         position, text, draw, font_size, bg_width, bg_height
#     ):
#         # Adjust the position based on the background size
#         text_position = (position[0] + bg_width // 2, position[1] + bg_height // 2)
#         # Draw the text background
#         draw.rectangle(
#             [position[0], position[1], position[0] + bg_width, position[1] + bg_height],
#             fill="white",
#         )
#         # Draw the text
#         draw.text(text_position, text, fill="black", font_size=font_size, anchor="mm")
#
#     # Draw vertical lines and labels at every `grid_interval` pixels
#     for x in range(grid_interval, width, grid_interval):
#         line = ((x, 0), (x, height))
#         draw.line(line, fill="blue")
#         for y in range(grid_interval, height, grid_interval):
#             # Calculate the percentage of the width and height
#             x_percent = round((x / width) * 100)
#             y_percent = round((y / height) * 100)
#             draw_label_with_background(
#                 (x - bg_width // 2, y - bg_height // 2),
#                 f"{x_percent}%,{y_percent}%",
#                 draw,
#                 font_size,
#                 bg_width,
#                 bg_height,
#             )
#
#     # Draw horizontal lines - labels are already added with vertical lines
#     for y in range(grid_interval, height, grid_interval):
#         line = ((0, y), (width, y))
#         draw.line(line, fill="blue")
#
#     # Save the image with the grid
#     image.save(new_image_path)

import os
import threading
import pyttsx3
import pyautogui
import pytesseract
from PIL import Image
from langdetect import detect
from gtts import gTTS
import pygame

from aura.core.utils import get_screenshot_file


def read_the_pdf():
    # take current screenshot using pyAutoGUI
    screenshot_file_path = get_screenshot_file()
    # screenshot = pyautogui.screenshot()
    # screenshot.save(screenshot_file_path)

    # alternative ---> https://pypi.org/project/indic-doctr/

    # set the tesseract command
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    with Image.open(screenshot_file_path) as img:
        text = pytesseract.image_to_string(img, lang='ori')
    print("text", text)

    # language detect using langdetect
    # language = detect(text)
    language = 'or'
    print("language", language)

    # Generate speech audio
    current_dir = os.getcwd()
    speech_file_path = os.path.join(current_dir, 'aura', 'assets', 'sounds', 'speech.mp3')
    os.makedirs(os.path.dirname(speech_file_path), exist_ok=True)

    print("speech file path", speech_file_path)
    # https://github.com/AI4Bharat/Indic-TTS/releases/tag/v1-checkpoints-release
    # https://github.com/AI4Bharat/Indic-TTS?tab=readme-ov-file

    # speech = gTTS(text=text, lang=language, slow=False)
    # speech.save(speech_file_path)
    # print("saved audio file")

    # # Initialize the pygame mixer
    # pygame.mixer.init()
    #
    # # Load the audio file
    # pygame.mixer.music.load(speech_file_path)
    #
    # # Play the audio file
    # pygame.mixer.music.play()
    #
    # # Keep the script running until the music finishes playing
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)

    return
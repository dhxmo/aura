import logging
import os

import speech_recognition as sr
from playsound import playsound

from .aura import init_aura


class SpeechRecognitionApp:
    def __init__(self):
        self.active = False
        self.r = sr.Recognizer()

        self.activate_voice_sound = 'start.mp3'
        self.deactivate_voice_sound = 'end.mp3'
        self.recognize_command_sound = 'new.mp3'

    def run(self):
        with sr.Microphone() as source:
            print("source", source)

            while True:  # Continuously listen for speech
                try:
                    audio = self.r.listen(source, timeout=5, phrase_time_limit=10)
                    if audio:
                        text = self.r.recognize_google(audio)
                        print("text", text)

                        if 'activate voice' in text and not self.active:
                            self.active = True
                            play_sound(self.activate_voice_sound)

                        elif 'deactivate voice' in text and self.active:
                            self.active = False
                            play_sound(self.deactivate_voice_sound)

                        elif self.active:
                            print(f"Recognized text: {text}")
                            play_sound(self.recognize_command_sound)

                            # initiate_aura(text)
                            init_aura(text)
                except Exception as e:
                    logging.info(f"Error occurred while _recognize_speech: {e}")
                    return


def play_sound(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'assets', 'audio', filename)
    playsound(file_path)

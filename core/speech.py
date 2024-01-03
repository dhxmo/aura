import os

import speech_recognition as sr
from playsound import playsound

from .aura import initiate_aura


class SpeechRecognitionApp:
    def __init__(self):
        self.active = False
        self.r = sr.Recognizer()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.activate_voice_sound = 'start.mp3'
        self.deactivate_voice_sound = 'end.mp3'
        self.recognize_command_sound = 'new.mp3'

    def run(self):
        self._recognize_speech()

    def _recognize_speech(self):
        with sr.Microphone() as source:
            while True:  # Continuously listen for speech
                audio = self.r.listen(source)
                if audio:
                    try:
                        text = self.r.recognize_google(audio)

                        if 'activate voice' in text and not self.active:
                            self.active = True
                            play_sound(self.activate_voice_sound)

                        elif 'deactivate voice' in text and self.active:
                            self.active = False
                            # playsound(self.deactivate_voice_sound)

                        elif self.active:
                            print(f"Recognized text: {text}")
                            # playsound(self.recognize_command_sound)

                            initiate_aura(text)

                    except Exception as e:
                        print(f"Error occurred: {e}")


def play_sound(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'assets', 'audio', filename)
    playsound(file_path)

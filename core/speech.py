import os

import speech_recognition as sr
from playsound import playsound


class SpeechRecognitionApp:
    def __init__(self):
        self.active = False
        self.r = sr.Recognizer()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.activate_voice_sound = os.path.join(base_dir, 'assets/audio/start.ogg')
        self.deactivate_voice_sound = os.path.join(base_dir, 'assets/audio/end.ogg')
        self.recognize_command_sound = os.path.join(base_dir, 'assets/audio/new.ogg')

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
                            playsound(self.activate_voice_sound)

                        elif 'deactivate voice' in text and self.active:
                            self.active = False
                            playsound(self.deactivate_voice_sound)

                        elif self.active:
                            print(f"Recognized text: {text}")
                            playsound(self.recognize_command_sound)

                    except Exception as e:
                        print(f"Error occurred: {e}")

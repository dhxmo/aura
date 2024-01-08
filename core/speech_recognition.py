import speech_recognition as sr

from .aura import init_aura
from .utils import play_sound


class AuraSpeechRecognition:
    def __init__(self):
        self.active = False
        self.r = sr.Recognizer()
        self.r.energy_threshold = 5000

        self.ready_sound = 'ready.mp3'
        self.activate_voice_sound = 'start.mp3'
        self.deactivate_voice_sound = 'end.mp3'
        self.recognize_command_sound = 'new.mp3'

    def run(self, driver):
        with sr.Microphone() as source:
            play_sound(self.ready_sound)

            while True:  # Continuously listen for speech
                audio = self.r.listen(source, phrase_time_limit=10)
                if audio:
                    try:
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

                            init_aura(text=text, driver=driver)
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand the audio")
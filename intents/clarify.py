import pyttsx3

from core.utils import play_sound


def clarify():
    play_sound("cancel.mp3")

    # Initialize the speech engine
    engine = pyttsx3.init()
    engine.say("Aura couldn't understand what you meant. Please speak slowly and clearly.")
    engine.runAndWait()
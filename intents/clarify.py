import pyttsx3


def clarify():
    # Initialize the speech engine
    engine = pyttsx3.init()
    engine.say("Aura couldn't understand what you meant. Please speak slowly and clearly.")
    engine.runAndWait()
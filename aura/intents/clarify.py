from aura.core.utils import play_sound, read_aloud


def clarify():
    play_sound("cancel.mp3")
    read_aloud("I couldn't understand what you meant. Please speak slowly and clearly.")
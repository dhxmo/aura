import platform

from aura.core.config import Config
from aura.core.utils import clean_up_intent, play_sound
from aura.engine.parser import parser
from aura.engine.runner import runner


def init_aura(text, driver):
    if platform.system() == "Windows":
        # intent = parser(payload=text, db_file=Config.db_file)
        intent = """command='read_the_pdf', detected_keyword=''"""
        print("intent", intent)

        intent_dict = clean_up_intent(intent)

        runner(intent_dict=intent_dict, driver=driver)
        return
    else:
        play_sound("Currently only Windows systems are supported.")
        return

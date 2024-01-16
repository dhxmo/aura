from aura.core.config import Config
from aura.core.utils import clean_up_intent
from aura.engine.parser import parser
from aura.engine.runner import runner


def init_aura(text, driver):
    intent = parser(payload=text, db_file=Config.db_file)
    print("intent", intent)

    intent_dict = clean_up_intent(intent)

    runner(intent_dict=intent_dict, driver=driver)
    return

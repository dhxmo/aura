from aura.core.config import Config
from aura.core.utils import clean_up_intent
from aura.engine.parser import parser, parse_user_input
from aura.engine.runner import runner
from aura.intents.free_flow import free_flow


def init_aura(text, driver):
    intent = parser(payload=text, db_file=Config.db_file)
    print("intent", intent)

    intent_dict = clean_up_intent(intent)

    # if intent_dict['command'] == 'free_flow':
    #     free_flow(user_action=intent_dict['detected_keyword'], driver=driver)
    # else:
    #     runner(intent_dict=intent_dict, driver=driver)

    runner(intent_dict=intent_dict, driver=driver)
    return

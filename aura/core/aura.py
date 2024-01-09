from aura.core.config import Config
from aura.engine.parser import parser
from aura.engine.runner import runner


def init_aura(text, driver):
    # intent = parser(payload=text, db_file=Config.db_file)
    intent = "command='submit_form', detected_keyword=''"
    runner(intent=intent, driver=driver)
    return

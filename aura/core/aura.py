from aura.core.config import Config
from aura.engine.parser import parser
from aura.engine.runner import runner


def init_aura(text, driver):
    # intent = parser(payload=text, db_file=Config.db_file)
    intent = "command='open_bookmark', detected_keyword='BuzzFeed Keto'"
    runner(intent=intent, driver=driver)
    return

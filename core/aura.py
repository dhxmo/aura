from core.config import Config
from engine.parser import parser
from engine.runner import runner


def init_aura(driver, text):
    # intent = parser(payload=text, db_file=Config.db_file)
    intent = "command='web_search', detected_keyword='mountains'"
    runner(driver=driver, intent=intent)

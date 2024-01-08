from core.config import Config
from engine.parser import parser
from engine.runner import runner


def init_aura(text, driver):
    # intent = parser(payload=text, db_file=Config.db_file)
    intent = "command='amazon_product_summary', detected_keyword=''"
    runner(intent=intent, driver=driver)
    return

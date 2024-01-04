from core.config import Config
from engine.parser import parser
from engine.runner import runner


def init_aura(text):
    # intent = parser(payload=text, db_file=Config.db_file)
    intent = "command='search', detected_keyword='google chrome'"

    runner(intent)

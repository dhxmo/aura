from core.config import Config
from engine.parser import parser
from engine.runner import runner


def init_aura(text, driver):
    # intent = parser(payload=text, db_file=Config.db_file)
    intent = "command='find_file_in_dir', detected_keyword='main.py', root_directory='D:\\operate'"
    runner(intent=intent, driver=driver)

from aura.core.config import Config
from aura.engine.parser import parser
from aura.engine.runner import runner


def init_aura(text, driver):
    # intent = parser(payload=text, db_file=Config.db_file)
    intent = "command='delete_promotional_n_socials', detected_keyword=''"
    runner(intent=intent, driver=driver)
    return


# hello, hope you're well. I'd like to buy some flowers. Regards.
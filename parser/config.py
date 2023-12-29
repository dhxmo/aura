from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
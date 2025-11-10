import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DJANGO_API_URL = os.getenv("DJANGO_API_URL")
    SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL_MINUTES", 15))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"


config = Config()

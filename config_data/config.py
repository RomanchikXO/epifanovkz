import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ID_adm")

DEFAULT_COMMANDS = [
    ("/start", "Начать работу с ботом"),
    ("/help", "Получить справку"),
]

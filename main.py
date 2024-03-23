from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from database import DataBase
from utils.getter_tasks_everyday import get_tasks_everyday
import threading
import schedule


def schedule_func():
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    for day in weekdays:
        schedule.every().day.at("07:55").do(get_tasks_everyday)


if __name__ == "__main__":
    DataBase.create_tables()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    threading.Thread(target=schedule_func).start()
    threading.Thread(target=bot.infinity_polling, args=(), kwargs={"skip_pending": True}).start()
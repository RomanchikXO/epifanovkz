from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from database import DataBase

import concurrent.futures
from utils.getter_tasks_everyday import get_tasks_everyday


if __name__ == "__main__":
    DataBase.create_tables()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    #используем многопоточность
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(get_tasks_everyday)
        executor.submit(bot.infinity_polling(skip_pending=True))



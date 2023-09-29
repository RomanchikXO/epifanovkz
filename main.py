from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from database import DataBase



if __name__ == "__main__":
    DataBase.create_tables()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()


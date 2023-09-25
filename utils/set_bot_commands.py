from telebot.types import BotCommand
from epifanov_clinic.config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    print(f'Дефолтные команды {[BotCommand(*i).command for i in DEFAULT_COMMANDS]}')
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
    print('Команды загружены\n')

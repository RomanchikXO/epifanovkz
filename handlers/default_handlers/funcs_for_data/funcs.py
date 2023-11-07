from loader import bot
from telebot.types import Message


def add_name_path(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_pat'] = message.text.title()
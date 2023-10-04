from telebot import types
from typing import Tuple


def done_for_task() -> Tuple[str, types.InlineKeyboardMarkup]:
    keyboard = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton("Выполнено", callback_data="confirm")
    keyboard.add(confirm_button)
    return keyboard
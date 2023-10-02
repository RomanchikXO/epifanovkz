from telebot import types
from typing import Tuple


def create_confirmation_keyboard(data: dict) -> Tuple[str, types.InlineKeyboardMarkup]:
    message_text = "Ваша информация:\n"
    message_text += f"Имя пациента: {data.get('name_pat', 'не указана')}\n"
    message_text += f"Дата выполнения задачи: {data.get('date_task', 'не указана')}\n"
    message_text += f"Задача: {data.get('task', 'не указана')}\n"

    keyboard = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton("Подтвердить", callback_data="confirm")
    change_button = types.InlineKeyboardButton("Изменить", callback_data="change_info")
    keyboard.add(change_button, confirm_button)

    return message_text, keyboard

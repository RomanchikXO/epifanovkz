from telebot import types


def done_for_task(name: str) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton("Выполнено", callback_data=name)
    keyboard.add(confirm_button)
    return keyboard
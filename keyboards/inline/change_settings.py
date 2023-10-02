from telebot import types


def create_change_buttom() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton(text="Имя пациента")
    button2 = types.KeyboardButton(text="Дата выполнения задачи")
    button3 = types.KeyboardButton(text="Задача")

    keyboard.add(button1, button2, button3)
    return keyboard


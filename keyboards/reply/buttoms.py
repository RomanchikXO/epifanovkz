from telebot import types


def create_keyboard_person():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("Кнопка 1")
    button2 = types.KeyboardButton("Кнопка 2")
    button3 = types.KeyboardButton("Кнопка 3")

    keyboard.add(button1, button2, button3)
    return keyboard


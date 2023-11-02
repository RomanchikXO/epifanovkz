from telebot import types


def create_keyboard_person():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("Администратор")
    button2 = types.KeyboardButton("Врач")
    button3 = types.KeyboardButton("Массажист")

    keyboard.add(button1, button2, button3)
    return keyboard


def name_staff(job):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if job == "adm":
        button1 = types.KeyboardButton("Анара")
        button2 = types.KeyboardButton("Кристина")
        keyboard.add(button1, button2)
    elif job == "doc":
        button1 = types.KeyboardButton("Денис")
        button2 = types.KeyboardButton("Мария")
        button3 = types.KeyboardButton("Жулдыз")
        keyboard.add(button1, button2, button3)
    elif job == "mas":
        button1 = types.KeyboardButton("Роман")
        button2 = types.KeyboardButton("Луиза")
        keyboard.add(button1, button2)

    return keyboard


def select_an_action(type_person):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("Добавить")
    button2 = types.KeyboardButton("Прочитать")

    if type_person == "adm":
        keyboard.add(button2)
    elif type_person == "docs":
        keyboard.add(button1, button2)
    return keyboard

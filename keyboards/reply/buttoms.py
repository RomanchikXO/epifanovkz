from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboard_person() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = KeyboardButton("Администратор")
    button2 = KeyboardButton("Врач")
    button3 = KeyboardButton("Массажист")

    keyboard.add(button1, button2, button3)
    return keyboard


def name_staff(job: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if job == "adm":
        button1 = KeyboardButton("Анара")
        button2 = KeyboardButton("Кристина")
        keyboard.add(button1, button2)
    elif job == "doc":
        button1 = KeyboardButton("Денис")
        button2 = KeyboardButton("Мария")
        button3 = KeyboardButton("Жулдыз")
        keyboard.add(button1, button2, button3)
    elif job == "mas":
        button1 = KeyboardButton("Роман")
        button2 = KeyboardButton("Луиза")
        keyboard.add(button1, button2)

    return keyboard


def select_an_action(type_person: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = KeyboardButton("Добавить")
    button2 = KeyboardButton("Прочитать")
    button3 = KeyboardButton("Мои задачи")

    if type_person == "adm":
        keyboard.add(button2)
    elif type_person == "docs":
        keyboard.add(button1, button2, button3)
    return keyboard

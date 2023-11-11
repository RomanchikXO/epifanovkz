from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def week_month_change() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = KeyboardButton("Неделя🔽")
    button2 = KeyboardButton("Месяц🔽")
    button3 = KeyboardButton("Ввод даты")
    button4 = KeyboardButton("Назад🔙")

    keyboard.add(button1, button2, button3, button4)
    return keyboard
from telebot.types import Message
from epifanov_clinic.loader import bot
from epifanov_clinic.keyboards.reply.buttoms import create_keyboard_person



@bot.message_handler(state="*", commands=["start"])
def bot_start(message: Message) -> None:
    print('Декоратор @bot.message_handler(commands=["start"]) сработал')
    change_keyboard = create_keyboard_person()
    bot.send_message(message.from_user.id, "Выберите, профессию:", reply_markup=change_keyboard)
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!"
                          f"Для вывода справки введите команду /help")

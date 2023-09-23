from telebot.types import Message
from loader import bot
from keyboards.reply.



@bot.message_handler(state="*", commands=["start"])
def bot_start(message: Message) -> None:
    print('Декоратор @bot.message_handler(commands=["start"]) сработал')
    change_keyboard = create_change_buttom()
    bot.send_message(message.from_user.id, "Выберите, какие данные нужно изменить:", reply_markup=change_keyboard)
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!"
                          f"Для вывода справки введите команду /help")

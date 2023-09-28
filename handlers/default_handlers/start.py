from telebot.types import Message
from loader import bot
from keyboards.reply.buttoms import create_keyboard_person
from states.person_info import UserInfoState


@bot.message_handler(state="*", commands=["start"])
def bot_start(message: Message) -> None:
    print('Декоратор @bot.message_handler(commands=["start"]) сработал')
    change_keyboard = create_keyboard_person()
    bot.set_state(message.from_user.id, UserInfoState.change_doc, message.chat.id)
    bot.send_message(message.from_user.id, "Выберите, профессию:", reply_markup=change_keyboard)



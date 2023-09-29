from telebot.types import Message
from loader import bot
from epifanovkz.keyboards.reply.buttoms import *
from epifanovkz.states.person_info import UserInfoState


@bot.message_handler(state="*", commands=["start"])
def bot_start(message: Message) -> None:
    print('Декоратор @bot.message_handler(commands=["start"]) сработал')
    change_keyboard = create_keyboard_person()
    bot.set_state(message.from_user.id, UserInfoState.change_staff, message.chat.id)
    bot.send_message(message.from_user.id, "Выберите, профессию:", reply_markup=change_keyboard)


@bot.message_handler(state=UserInfoState.change_staff, func=lambda message: message.text in ["Администратор", "Врач", "Массажист"])
def handle_button_click(message):
    if message.text == "Администратор":
        bot.set_state(message.from_user.id, UserInfoState.change_name, message.chat.id)
        change_keyboard = create_keyboard_adm()
        bot.send_message(message.from_user.id, "Выбери специалиста", reply_markup=change_keyboard)
    elif message.text == "Врач":
        bot.set_state(message.from_user.id, UserInfoState.change_name, message.chat.id)
        change_keyboard = create_keyboard_doc()
        bot.send_message(message.from_user.id, "Выбери специалиста", reply_markup=change_keyboard)
    elif message.text == "Массажист":
        bot.set_state(message.from_user.id, UserInfoState.change_name, message.chat.id)
        change_keyboard = create_keyboard_mas()
        bot.send_message(message.from_user.id, "Выбери специалиста", reply_markup=change_keyboard)



@bot.message_handler(state=UserInfoState.change_name, func=lambda message: message.text in ["Анара", "Кристина", "Денис", "Мария", "Жулдыз", "Роман", "Луиза"])
def handle_button_click(message):
        if message.text == "Анара":
            pass
        elif message.text == "Кристина":
            pass
        elif message.text == "Денис":
            pass
        elif message.text == "Мария":
            pass
        elif message.text == "Роман":
            bot.send_message(message.from_user.id, f'{message.from_user.id} Это твой id')
        elif message.text == "Луиза":
            pass

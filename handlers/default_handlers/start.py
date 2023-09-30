from telebot.types import Message
from loader import bot
from keyboards.reply.buttoms import *
from states.person_info import UserInfoState
from database.DataBase import User, Tasks


@bot.message_handler(state="*", commands=["start"])
def bot_start(message: Message) -> None:
    print('Декоратор @bot.message_handler(commands=["start"]) сработал')
    change_keyboard = create_keyboard_person()
    bot.set_state(message.from_user.id, UserInfoState.change_staff, message.chat.id)
    bot.send_message(message.from_user.id, "Выберите, профессию:", reply_markup=change_keyboard)


@bot.message_handler(state=UserInfoState.change_staff,
                     func=lambda message: message.text in ["Администратор", "Врач", "Массажист"])
def handle_button_click(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data.clear()
        data['status'] = message.text
        data['tele_id'] = message.from_user.id
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
        else:
            bot.send_message(message.from_user.id, "Ошибка ввода, повторите попытку")


@bot.message_handler(state=UserInfoState.change_name,
                     func=lambda message: message.text in ["Анара", "Кристина", "Денис", "Мария", "Жулдыз", "Роман",
                                                           "Луиза"])
def handle_button_click(message):

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        existing_person: object = User.get_or_none(name=message.text, telegram_id=data['tele_id'], profession=data['status'])
        if existing_person is None:
            User.create(name=message.text, telegram_id=data['tele_id'], profession=data['status'])

    queryset = User.select().where(User.status == data['tele_id'])

    for person in queryset:
        name = person.name
        tg_id = person.telegram_id

    if message.text == "Анара":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')


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

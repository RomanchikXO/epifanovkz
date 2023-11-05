from handlers.default_handlers.adder_task import *

import peewee
from telebot.types import Message
from loader import bot

from keyboards.reply.buttoms import *
from keyboards.inline.completed_or_not import *

from states.person_info import UserInfoState
from database.DataBase import User, Tasks
import datetime



# with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#    data['profession'] = message.text
#    data['tele_id'] = message.from_user.id
#    data['date_task'] = result
#    data['task'] = message.text.capitalize()
#    data["name_patient"] = call.data

@bot.message_handler(state="*", commands=["start"])
def bot_start(message: Message) -> None:
    print('Декоратор @bot.message_handler(commands=["start"]) сработал')
    change_keyboard = create_keyboard_person()
    bot.set_state(message.from_user.id, UserInfoState.change_staff, message.chat.id)
    bot.send_message(message.from_user.id, "Выберите свою профессию:", reply_markup=change_keyboard)


@bot.message_handler(state=UserInfoState.change_staff,
                     func=lambda message: message.text in ["Администратор", "Врач", "Массажист"])
def handle_button_click(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data.clear()
        data['profession'] = message.text
        data['tele_id'] = message.from_user.id

        bot.set_state(message.from_user.id, UserInfoState.change_name, message.chat.id)
        if message.text == "Администратор":
            change_keyboard = name_staff("adm")
        elif message.text == "Врач":
            change_keyboard = name_staff("doc")
        elif message.text == "Массажист":
            change_keyboard = name_staff("mas")

        bot.send_message(message.from_user.id, "Выбери специалиста", reply_markup=change_keyboard)


@bot.message_handler(state=UserInfoState.change_name,
                     func=lambda message: message.text in ["Анара", "Кристина", "Денис", "Мария", "Жулдыз", "Роман",
                                                           "Луиза"])
def handle_button_click(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            existing_people = User.get(User.telegram_id == data['tele_id'])
        except peewee.DoesNotExist:
            # Создаем нового пользователя, если запись не существует
            User.create(name=message.text, telegram_id=data['tele_id'], profession=data['profession'])
        finally:
            # Снова получаем существующих пользователей (или только что созданного)
            existing_people = User.select().where(User.telegram_id == data['tele_id'])

            name = None
            for person in existing_people:
                name = person.name

            if message.text == name:
                bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
                bot.set_state(message.from_user.id, UserInfoState.add_info, message.chat.id)
                if message.text in ["Анара", "Кристина"]:
                    change_keyboard = select_an_action("adm")
                else:
                    change_keyboard = select_an_action("docs")
                bot.send_message(message.from_user.id, "Выбери задачу", reply_markup=change_keyboard)
            else:
                bot.send_message(message.from_user.id, f'Вы {name}')
                bot_start(message)


@bot.message_handler(state=UserInfoState.add_info,
                     func=lambda message: message.text in ["Добавить", "Прочитать"])
def add_and_view(message):
    if message.text == "Добавить":
        bot.set_state(message.from_user.id, UserInfoState.change_date, message.chat.id)
        handle_calendar_input(message)

    elif message.text == "Прочитать":
        print('Сейчас будем читать задачи')
        bot.set_state(message.from_user.id, UserInfoState.read_task, message.chat.id)
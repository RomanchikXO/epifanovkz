from .adder_task import handle_calendar_input
from .reader_task import read_task_func
from .docs_tasks import time_interval

import datetime

import peewee

from telebot.types import Message
from loader import bot

from keyboards.reply.buttoms import *

from states.person_info import UserInfoState
from database.DataBase import User


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
def handle_button_click(message: Message) -> None:
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
def handle_button_click(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            existing_people = User.get(User.telegram_id == data['tele_id'])
        except peewee.DoesNotExist:
            # Создаем нового пользователя, если запись не существует
            User.create(name=message.text, telegram_id=data['tele_id'], profession=data['profession'])
        finally:
            # Снова получаем существующих пользователей (или только что созданного)
            existing_people = User.select().where(User.telegram_id == data['tele_id'])

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


@bot.message_handler(state=[UserInfoState.add_info, UserInfoState.add_comment],
                     func=lambda message: message.text in ["Добавить", "Прочитать", "Мои задачи"])
def add_and_view(message: Message) -> None:

    if message.text == "Добавить":
        existing_people = User.select().where(User.profession in ["Врач", "Массажист"])
        some_list = [person.telegram_id for person in existing_people]
        if message.from_user.id in some_list:
            bot.set_state(message.from_user.id, UserInfoState.change_date, message.chat.id)
            handle_calendar_input(message)
        else:
            bot.send_message(message.from_user.id, "Добавление задач для вас не доступно")
    elif message.text == "Прочитать":
        print(f"Сейчас будем читать задачи {datetime.datetime.now()}")
        bot.set_state(message.from_user.id, UserInfoState.read_task, message.chat.id)
        read_task_func(message)
    elif message.text == "Мои задачи":
        print(f"Выведение задач {datetime.datetime.now()}")
        bot.set_state(message.from_user.id, UserInfoState.change_period, message.chat.id)
        time_interval(message)
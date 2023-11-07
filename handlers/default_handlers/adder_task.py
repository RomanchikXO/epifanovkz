import telebot
from .funcs_for_data.funcs import *
from loader import bot

from keyboards.inline.done_or_change import *
from keyboards.inline.change_settings import *

from telebot.types import Message, CallbackQuery
from typing import Union

from states.person_info import UserInfoState
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime

from keyboards.reply.buttoms import select_an_action

from database.DataBase import Tasks


@bot.message_handler(state=UserInfoState.change_date)
@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def handle_calendar_input(message_or_call: Union[Message, CallbackQuery]) -> None:
    if isinstance(message_or_call, Message):
        calendar, step = DetailedTelegramCalendar(locale='ru', min_date=datetime.date.today()).build()
        bot.send_message(message_or_call.chat.id,
                         f"Select {LSTEP[step]}",
                         reply_markup=calendar)
    elif isinstance(message_or_call, CallbackQuery):
        call = message_or_call
        result, key, step = DetailedTelegramCalendar().process(call.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            with bot.retrieve_data(call.from_user.id) as data:
                if data.get('date_task', None) is None:
                    data['date_task'] = result
                    bot.set_state(call.from_user.id, UserInfoState.change_pat_name)
                    bot.send_message(call.from_user.id, 'Введите ФАМИЛИЮ и ИМЯ пациента:')
                else:
                    print('Дату поменяли')
                    data['date_task'] = result
                    add_task(call, flag=False)


@bot.message_handler(state=UserInfoState.change_pat_name)
def pat_name(message: Message, flag: bool = True) -> None:
    add_name_path(message)
    if flag:
        bot.set_state(message.from_user.id, UserInfoState.change_task, message.chat.id)
        bot.send_message(message.from_user.id, 'Напишите задачу:')
    if not flag:
        print('Имя пациента поменяли')
        add_task(message, flag=False)


@bot.message_handler(state=UserInfoState.change_task)
def add_task(message: Message, flag: bool = True) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        if flag:
            data['task'] = message.text.capitalize()
        info_message, confirmation_keyboard = create_confirmation_keyboard(data)
    bot.set_state(message.from_user.id, UserInfoState.amendment)
    bot.send_message(message.from_user.id, info_message, reply_markup=confirmation_keyboard)


@bot.callback_query_handler(state=UserInfoState.amendment, func=lambda call: call.data == "change_info")
def confirm_data(call: CallbackQuery) -> None:
    change_keyboard = create_change_buttom()
    bot.send_message(call.message.chat.id, "Выберите, какие данные нужно изменить:", reply_markup=change_keyboard)
    bot.set_state(call.from_user.id, UserInfoState.changing_settings)


@bot.message_handler(state=UserInfoState.changing_settings,
                     func=lambda message: message.text in ["Имя пациента", "Дата выполнения задачи", "Задача"])
def handle_button_click(message: Message) -> None:
    if message.text == "Имя пациента":
        def get_name(message):
            pat_name(message, flag=False)

        bot.send_message(message.chat.id, "Введите ФАМИЛИЮ и ИМЯ пацента:")
        bot.register_next_step_handler(message, get_name)

    elif message.text == "Дата выполнения задачи":
        def get_date_task(message):
            handle_calendar_input(message, flag=False)

        bot.send_message(message.from_user.id, 'Введите дату выполнения задачи:')
        handle_calendar_input(message)
    elif message.text == "Задача":
        def get_task(message):
            add_task(message, flag=True)

        bot.send_message(message.from_user.id, 'Введите новую задачу:')
        bot.register_next_step_handler(message, get_task)


@bot.callback_query_handler(state=UserInfoState.amendment, func=lambda call: call.data == "confirm")
def confirm_data(call: CallbackQuery) -> None:
    print('Идет запись данных в бд')
    with bot.retrieve_data(call.from_user.id) as data:
        Tasks.create(name_patient=data["name_pat"], task=data['task'], date=data['date_task'], status=None,
                     comment_if_done=None)
        del data["name_pat"], data['task'], data['date_task']
    bot.send_message(call.from_user.id, "Ваши данные записаны")
    bot.set_state(call.from_user.id, UserInfoState.add_info)
    change_keyboard = select_an_action("docs")
    bot.send_message(call.from_user.id, "Выбери задачу", reply_markup=change_keyboard)
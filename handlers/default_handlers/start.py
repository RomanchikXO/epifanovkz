import telebot
from telebot.types import Message
from .funcs_for_data.funcs import *
from loader import bot

from keyboards.reply.buttoms import *
from keyboards.inline.done_or_change import *
from keyboards.inline.change_settings import *
from keyboards.inline.completed_or_not import *

from states.person_info import UserInfoState
from database.DataBase import User, Tasks
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime


# with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#    data['profession'] = message.text
#    data['tele_id'] = message.from_user.id
#    data['date_task'] = result
#    data['task'] = message.text.capitalize()

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
        data['profession'] = message.text
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
        existing_people = User.select().where(User.telegram_id == data['tele_id']).execute()

        if not existing_people:
            User.create(name=message.text, telegram_id=data['tele_id'], profession=data['profession'])
        existing_people = User.select().where(User.telegram_id == data['tele_id']).execute()

        name = None
        tg_id = None
        for person in existing_people:
            name = person.name
            tg_id = person.telegram_id

        if message.text in ["Анара", "Кристина"]:
            if message.text == name:
                bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
                bot.set_state(message.from_user.id, UserInfoState.add_info, message.chat.id)
                change_keyboard = select_an_action("adm")
                bot.send_message(message.from_user.id, "Выбери задачу", reply_markup=change_keyboard)
            else:
                bot.send_message(message.from_user.id, f'Вы {name}')
                bot_start(message)

        elif message.text in ["Роман", "Жулдыз", "Мария", "Денис", "Луиза"]:
            if message.text == name:
                bot.send_message(message.from_user.id, f'Вы действительно {message.text}')

                bot.set_state(message.from_user.id, UserInfoState.add_info, message.chat.id)
                change_keyboard = select_an_action("docs")
                bot.send_message(message.from_user.id, "Выбери задачу", reply_markup=change_keyboard)
            else:
                bot.send_message(message.from_user.id, f'Вы {name}')
                bot_start(message)
        elif message.text == "Луиза":
            if message.text == name:
                bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
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
        tasks_today = Tasks.select().where(Tasks.date == datetime.date.today()).execute()
        if tasks_today:
            for i_task in tasks_today:
                button = done_for_task()
                bot.set_state(message.from_user.id, UserInfoState.add_comment)
                with bot.retrieve_data(message.from_user.id) as data:
                    params = User.select().where(User.telegram_id == message.from_user.id).execute()
                    for param in params:
                        prof = param.profession
                        name = param.name
                if prof == "Администратор" or name in ["Роман", "Анара", "Кристина"]:
                    if not i_task.status:
                        bot.send_message(message.from_user.id, f'Пациент: {i_task.name_patient} - {i_task.task}',
                                         reply_markup=button)
                    else:
                        bot.send_message(message.from_user.id,  f'Пациент: {i_task.name_patient} - {i_task.task}\n'
                                                                f'Комментарий: {i_task.comment_if_done}')
                else:
                    bot.send_message(message.from_user.id, "Добавление комментариев доступно только для администраторов")

        else:
            bot.send_message(message.from_user.id, 'Задач на сегодня нет, можно чилить ^^)')


@bot.callback_query_handler(state=UserInfoState.add_comment, func=lambda call: call.data == "confirm")
def handle_callback(call, name):
    bot.set_state(call.from_user.id, UserInfoState.add_comment_2)
    bot.send_message(call.from_user.id, "Задача будет выполнена после добавления комментария. "
                                        "\nНапишите комментарий", name=name)


@bot.message_handler(state=UserInfoState.add_comment_2)
def handle_callback(message, name):
    Tasks.update(comment_if_done=message).where(Tasks.name_patient == name, Tasks.date == datetime.date.today()).execute()
    bot.send_message(message.from_user.id, "Комментарий успешно добавлен")
    bot.register_next_step_handler(message, add_and_view)


@bot.message_handler(state=UserInfoState.change_date)
@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def handle_calendar_input(message_or_call):
    if isinstance(message_or_call, telebot.types.Message):
        calendar, step = DetailedTelegramCalendar(locale='ru', min_date=datetime.date.today()).build()
        bot.send_message(message_or_call.chat.id,
                         f"Select {LSTEP[step]}",
                         reply_markup=calendar)
    elif isinstance(message_or_call, telebot.types.CallbackQuery):
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
def pat_name(message, flag=True):
    add_name_path(message)
    if flag:
        bot.set_state(message.from_user.id, UserInfoState.change_task, message.chat.id)
        bot.send_message(message.from_user.id, 'Напишите задачу:')
    if not flag:
        print('Имя пациента поменяли')
        add_task(message, flag=False)


@bot.message_handler(state=UserInfoState.change_task)
def add_task(message, flag=True):
    with bot.retrieve_data(message.from_user.id) as data:
        if flag:
            data['task'] = message.text.capitalize()
        info_message, confirmation_keyboard = create_confirmation_keyboard(data)
    bot.set_state(message.from_user.id, UserInfoState.amendment)
    bot.send_message(message.from_user.id, info_message, reply_markup=confirmation_keyboard)


@bot.callback_query_handler(state=UserInfoState.amendment, func=lambda call: call.data == "change_info")
def confirm_data(call):
    change_keyboard = create_change_buttom()
    bot.send_message(call.message.chat.id, "Выберите, какие данные нужно изменить:", reply_markup=change_keyboard)
    bot.set_state(call.from_user.id, UserInfoState.changing_settings)


@bot.message_handler(state=UserInfoState.changing_settings,
                     func=lambda message: message.text in ["Имя пациента", "Дата выполнения задачи", "Задача"])
def handle_button_click(message):
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
def confirm_data(call):
    print('Идет запись данных в бд')
    with bot.retrieve_data(call.from_user.id) as data:
        Tasks.create(name_patient=data["name_pat"], task=data['task'], date=data['date_task'], status=None,
                     comment_if_done=None)
    bot.send_message(call.from_user.id, "Ваши данные записаны")
    bot.set_state(call.from_user.id, UserInfoState.add_info)
    change_keyboard = select_an_action("docs")
    bot.send_message(call.from_user.id, "Выбери задачу", reply_markup=change_keyboard)

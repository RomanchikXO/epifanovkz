from telebot.types import Message
from loader import bot
from keyboards.reply.buttoms import *

from states.person_info import UserInfoState
from database.DataBase import User, Tasks
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime



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
        existing_person: object = User.get_or_none(name=message.text, telegram_id=data['tele_id'], profession=data['profession'])
        if existing_person is None:
            User.create(name=message.text, telegram_id=data['tele_id'], profession=data['profession'])

    queryset = User.select().where(User.profession == data['profession'])
    name = None
    tg_id = None
    for person in queryset:
        name = person.name
        tg_id = person.telegram_id

    if message.text == "Анара":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')


    elif message.text == "Анара":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')
    elif message.text == "Кристина":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')
    elif message.text == "Денис":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')
    elif message.text == "Мария":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')
    elif message.text == "Жулдыз":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')
    elif message.text == "Роман":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')

            bot.set_state(message.from_user.id, UserInfoState.add_info, message.chat.id)
            change_keyboard = add_task()
            bot.send_message(message.from_user.id, "Выбери задачу", reply_markup=change_keyboard)
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')
    elif message.text == "Луиза":
        if message.from_user.id == tg_id:
            bot.send_message(message.from_user.id, f'Вы действительно {message.text}')
        else:
            bot.send_message(message.from_user.id, f'Вы {name}')


@bot.message_handler(state=UserInfoState.add_info,
                     func=lambda message: message.text in ["Добавить", "Прочитать"])
def add_and_view(message):
    if message.text == "Добавить":
        bot.set_state(message.from_user.id, UserInfoState.change_date, message.chat.id)

        # Tasks.create(name=message.text, telegram_id=data['tele_id'], profession=data['profession'])
    elif message.text == "Прочитать":
        tasks_today = Tasks.select().where(Tasks.date == datetime.date.today())
        for i_task in tasks_today:
            bot.send_message(message.from_user.id, f'Пациент: {i_task.name_patient} - {i_task.task}')


@bot.message_handler(state=UserInfoState.change_date)
def butt_calendar(message):
    calendar, step = DetailedTelegramCalendar(locale='ru', min_date=datetime.date.today()).build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(call):
    result, key, step = DetailedTelegramCalendar().process(call.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              call.message.chat.id,
                              call.message.message_id)


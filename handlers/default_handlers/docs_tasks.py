import io
from loader import bot

from states.person_info import UserInfoState

from keyboards.reply.time_buttons import *
from keyboards.inline.completed_or_not import *

from database.DataBase import Tasks
from datetime import date, timedelta
from keyboards.reply.buttoms import select_an_action

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from telebot.types import Message

import datetime

def generate_tasks_report(days: int, chat_id: int, caption: str, visible_file_name: str) -> None:
    """
    Генерирует отчет о задачах за указанное количество дней и отправляет его в чат.

    :param days: Количество дней для фильтрации задач
    :type days: int

    :param chat_id: Уникальный идентификатор чата
    :type chat_id: int

    :param caption: Подпись к документу
    :type caption: str

    :param visible_file_name: Имя файла, видимое для пользователя
    :type visible_file_name: str

    :return: None
    :rtype: None
    """
    start_date = date.today() - timedelta(days=days)
    end_date = date.today()
    tasks_last_week = Tasks.select().where((Tasks.date >= start_date) & (Tasks.date <= end_date)).order_by(Tasks.date.desc())

    if tasks_last_week:
        file_content = '\n'.join(
            f"Врач:{i_task.doc}\nПациент:{i_task.name_patient}\nЗадача:{i_task.task}\nДата:{i_task.date}\nКомментарий:{i_task.comment_if_done}\n" for i_task in
            tasks_last_week)

        with io.BytesIO() as file:
            file.write(file_content.encode())
            file.seek(0)

            bot.send_document(
                chat_id=chat_id,
                document=file,
                caption=caption,
                visible_file_name=visible_file_name
            )
    else:
        bot.send_message(chat_id, f"Задачи за последние {days} отсутствуют.")

@bot.message_handler(state=UserInfoState.change_period,
                     func=lambda message: message.text == "Мои задачи")
def time_interval(message: Message) -> None:
    """
    Обработчик сообщений для изменения периода просмотра задач пользователя.

    При получении сообщения "Мои задачи" устанавливает состояние пользователя в UserInfoState.get_data.
    Затем отправляет сообщение с клавиатурой выбора периода просмотра задач или выбора даты.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return: None
    """
    bot.set_state(message.from_user.id, UserInfoState.get_data)
    change_keyboard = week_month_change()
    bot.send_message(message.from_user.id, "Выбери период просмотра задач или выбери дату", reply_markup=change_keyboard)


@bot.message_handler(state=UserInfoState.get_data,
                     func=lambda message: message.text in ["Неделя🔽", "Месяц🔽", "Ввод даты", "Назад🔙"])
def fetch_patient_data(message: Message) -> None:
    if message.text == "Неделя🔽":
        generate_tasks_report(
            days=7,
            chat_id=message.from_user.id,
            caption="Ваши задачи за последнюю неделю",
            visible_file_name="Задачи_неделя.txt"
        )
    elif message.text == "Месяц🔽":
        generate_tasks_report(
            days=30,
            chat_id=message.from_user.id,
            caption="Ваши задачи за последний месяц",
            visible_file_name="Задачи_месяц.txt"
        )
    elif message.text == "Ввод даты":
        bot.set_state(message.from_user.id, UserInfoState.get_date, message.chat.id)
        date_input(message)
    elif message.text == "Назад🔙":
        bot.set_state(message.from_user.id, UserInfoState.add_info, message.chat.id)
        change_keyboard = select_an_action("docs")
        bot.send_message(message.from_user.id, "Выбери задачу", reply_markup=change_keyboard)


@bot.message_handler(state=UserInfoState.get_date)
def date_input(message: Message) -> None:
    """
    Обработчик для ввода даты через календарь.

    :param message: Объект сообщения.
    :return: Ничего не возвращает.
    """
    calendar, step = DetailedTelegramCalendar(calendar_id=1, locale='ru', min_date=datetime.date.today()).build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def cal(call):
    result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru', min_date=datetime.date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        tasks_in_result = Tasks.select().where(Tasks.date == result).execute()
        with bot.retrieve_data(call.from_user.id) as data:
            data['date_task'] = result
        bot.set_state(call.from_user.id, UserInfoState.get_data)
        if tasks_in_result:
            for i_task in tasks_in_result:
                button = done_for_task(i_task.name_patient)
                bot.send_message(call.from_user.id, f'Врач: {i_task.doc}\n'
                                                    f'Пациент: {i_task.name_patient} \n'
                                                    f'Задача: {i_task.task} \n'
                                                    f'Комментарий: {i_task.comment_if_done}',
                                 reply_markup=button)

        else:
            bot.send_message(call.from_user.id, 'Задач на эту дату нет')


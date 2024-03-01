import time

from loader import bot
from keyboards.inline.completed_or_not import *

from states.person_info import UserInfoState
from database.DataBase import Tasks, db
import datetime


admin_kris = 1113592485


def get_tasks_everyday() -> None:
    """
    Вывод задач на сегодня.

    :return: Ничего не возвращает.
    """
    while True:
        tasks_today = Tasks.select().where(Tasks.date == datetime.date.today()).execute()
        now = datetime.datetime.now()

        if now.weekday() != 6 and now.hour == 7 and now.minute == 59:
            if tasks_today:
                for i_task in tasks_today:
                    button = done_for_task(i_task.name_patient)

                    bot.set_state(admin_kris, UserInfoState.add_comment)

                    if i_task.status is None:
                        bot.send_message(admin_kris, f'Пациент: {i_task.name_patient} \nЗадача: {i_task.task}',
                                         reply_markup=button)
                        with bot.retrieve_data(admin_kris) as data:
                            data['date_task'] = datetime.date.today()
                    else:
                        bot.send_message(admin_kris, f'Пациент: {i_task.name_patient} - {i_task.task}\n'
                                                               f'Комментарий✅: {i_task.comment_if_done}')
            else:
                bot.set_state(admin_kris, UserInfoState.add_info)
                bot.send_message(admin_kris, 'Задач на сегодня нет, можно чилить ^^)')

            # Вычисляем количество секунд до следующего дня
            tomorrow = now + datetime.timedelta(days=1)
            seconds_until_tomorrow = (tomorrow - datetime.datetime.now()).total_seconds()
            # Засыпаем на это количество секунд
            time.sleep(seconds_until_tomorrow)





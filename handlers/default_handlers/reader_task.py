from loader import bot
from start import add_and_view
from keyboards.inline.completed_or_not import *

from states.person_info import UserInfoState
from database.DataBase import User, Tasks
import datetime

@bot.message_handler(state=UserInfoState.read_task,
                     func=lambda message: message.text == "Прочитать")
def read_task_func(message):
    tasks_today = Tasks.select().where(Tasks.date == datetime.date.today()).execute()

    if tasks_today:
        for i_task in tasks_today:
            button = done_for_task(i_task.name_patient)

            bot.set_state(message.from_user.id, UserInfoState.add_comment)

            params = User.select().where(User.telegram_id == message.from_user.id).execute()
            for param in params:
                prof = param.profession
                name = param.name

            if i_task.status is None:
                bot.send_message(message.from_user.id, f'Пациент: {i_task.name_patient} - {i_task.task}',
                                 reply_markup=button)
            else:
                bot.send_message(message.from_user.id,  f'Пациент: {i_task.name_patient} - {i_task.task}\n'
                                                        f'Комментарий: {i_task.comment_if_done}')
    else:
        bot.send_message(message.from_user.id, 'Задач на сегодня нет, можно чилить ^^)')


@bot.callback_query_handler(state=UserInfoState.add_comment, func=lambda call: True)
def handle_callback(call):
    with bot.retrieve_data(call.from_user.id) as data:
        data["name_patient"] = call.data
    bot.set_state(call.from_user.id, UserInfoState.add_comment_2)
    bot.send_message(call.from_user.id, "Задача будет выполнена после добавления комментария. "
                                        "\nНапишите комментарий")


@bot.message_handler(state=UserInfoState.add_comment_2)
def handle_callback(message):
    print('сейчас добавится коммент')
    with bot.retrieve_data(message.from_user.id) as data:
        print(f'для {data["name_patient"]}')
        Tasks.update(comment_if_done=message.text, status=True).where(Tasks.name_patient == data["name_patient"], Tasks.date == datetime.date.today()).execute()
    bot.send_message(message.from_user.id, "Комментарий успешно добавлен")
    bot.register_next_step_handler(message, add_and_view)
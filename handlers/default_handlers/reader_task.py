from loader import bot
from keyboards.inline.completed_or_not import *
from telebot.types import Message, CallbackQuery

from states.person_info import UserInfoState
from database.DataBase import User, Tasks
import datetime

from keyboards.reply.buttoms import select_an_action


@bot.message_handler(state=[UserInfoState.read_task, UserInfoState.add_comment],
                     func=lambda message: message.text == "Прочитать")
def read_task_func(message: Message) -> None:
    """
    Обработчик для вывода задач на сегодня.

    :param message: Объект сообщения от пользователя.
    :return: Ничего не возвращает.
    """
    tasks_today = Tasks.select().where(Tasks.date == datetime.date.today()).execute()

    if tasks_today:
        for i_task in tasks_today:
            button = done_for_task(i_task.name_patient)

            bot.set_state(message.from_user.id, UserInfoState.add_comment)

            if i_task.status is None:
                bot.send_message(message.from_user.id, f'Пациент: {i_task.name_patient} \nЗадача: {i_task.task}',
                                 reply_markup=button)
                with bot.retrieve_data(message.from_user.id) as data:
                    data['date_task'] = datetime.date.today()
            else:
                bot.send_message(message.from_user.id,  f'Пациент: {i_task.name_patient} - {i_task.task}\n'
                                                        f'Комментарий✅: {i_task.comment_if_done}')
    else:
        bot.set_state(message.from_user.id, UserInfoState.add_info)
        bot.send_message(message.from_user.id, 'Задач на сегодня нет, можно чилить ^^)')


@bot.callback_query_handler(state=[UserInfoState.add_comment, UserInfoState.add_info, UserInfoState.get_data], func=lambda call: True)
def handle_callback(call: CallbackQuery) -> None:
    with bot.retrieve_data(call.from_user.id) as data:
        data["name_patient"] = call.data
    bot.set_state(call.from_user.id, UserInfoState.add_comment_2)
    bot.send_message(call.from_user.id, "Задача будет выполнена после добавления комментария. "
                                        "\nНапишите комментарий")


@bot.message_handler(state=UserInfoState.add_comment_2)
def handle_callback(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        Tasks.update(comment_if_done=message.text, status=True).where(Tasks.name_patient == data["name_patient"],
                                                                      Tasks.date == data['date_task']).execute()
        data.clear()
        data['date_task'] = datetime.date.today()

    bot.send_message(message.from_user.id, "Комментарий успешно добавлен")
    bot.set_state(message.from_user.id, UserInfoState.add_info)

    customer_prof = User.select().where(User.telegram_id == message.from_user.id)[0].profession
    if customer_prof == "Администратор":
        change_keyboard = select_an_action("adm")
    else:
        change_keyboard = select_an_action("docs")
    bot.send_message(message.from_user.id, "Выбери задачу", reply_markup=change_keyboard)
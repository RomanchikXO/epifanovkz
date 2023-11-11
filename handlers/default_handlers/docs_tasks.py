import io
from loader import bot
from telebot.types import Message
from states.person_info import UserInfoState
from keyboards.reply.time_buttons import *
from database.DataBase import User, Tasks
from datetime import date, timedelta


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
    tasks_last_week = Tasks.select().where((Tasks.date >= start_date) & (Tasks.date <= end_date)).execute()

    file_content = '\n'.join(
        f"{i_task.name_patient} - {i_task.task} - {i_task.date} - {i_task.comment_if_done}\n" for i_task in
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


@bot.message_handler(state=UserInfoState.change_period,
                     func=lambda message: message.text == "Мои задачи")
def time_interval(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.get_data)
    change_keyboard = week_month_change()
    bot.send_message(message.from_user.id, "Выбери период просмотра задач или выбери дату", reply_markup=change_keyboard)


@bot.message_handler(state=UserInfoState.get_data,
                     func=lambda message: message.text in ["Неделя🔽", "Месяц🔽", "Ввод даты"])
def fetch_patient_data(message: Message) -> None:
    if message.text == "Неделя🔽":
        generate_tasks_report(
            days=7,
            chat_id = message.from_user.id,
            caption = "Ваши задачи за последнюю неделю",
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
        bot.send_message(message.from_user.id, "Пока в разработке")
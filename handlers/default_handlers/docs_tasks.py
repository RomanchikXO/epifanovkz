from loader import bot
from telebot.types import Message
from states.person_info import UserInfoState
from keyboards.reply.time_buttons import *


@bot.message_handler(state=UserInfoState.change_period,
                     func=lambda message: message.text == "Мои задачи")
def time_interval(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.get_data)
    change_keyboard = week_month_change()
    bot.send_message(message.from_user.id, "Выбери период просмотра задач или выбери дату", reply_markup=change_keyboard)


@bot.message_handler(state=UserInfoState.get_data,
                     func=lambda message: message.text in ["Неделя", "Месяц", "Ввод даты"])
def fetch_patient_data(message: Message) -> None:
    if message.text == "Неделя":
        pass
    elif message.text == "Месяц":
        pass
    elif message.text == "Ввод даты":
        pass
from telebot.handler_backends import State, StatesGroup

class UserInfoState(StatesGroup):
    change_staff = State()
    change_name = State()
    add_info = State()
    viewing_information = State()

    change_date = State()
from telebot.handler_backends import State, StatesGroup

class UserInfoState(StatesGroup):
    change_staff = State()
    change_name = State()
    change_doc = State()
    change_mas = State()
    add_info = State()
    viewing_information = State()
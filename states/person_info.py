from telebot.handler_backends import State, StatesGroup

class UserInfoState(StatesGroup):
    change_staff = State()
    change_doc = State()
    change_massage = State()
    add_info = State()
    viewing_information = State()
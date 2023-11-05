from telebot.handler_backends import State, StatesGroup

class UserInfoState(StatesGroup):
    change_staff = State()
    change_name = State()
    add_info = State()
    viewing_information = State()

    change_date = State()
    change_pat_name = State()
    change_task = State()
    changing_settings = State()
    amendment = State()

    read_task = State()
    add_comment = State()
    add_comment_2 = State()

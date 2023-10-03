from loader import bot

def add_name_path(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_pat'] = message.text.title()
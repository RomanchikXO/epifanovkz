from telebot.types import Message
from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    bot.reply_to(
        message, "Я вас не понимаю, давай попробуем сначала\n"
                 "Нажми сюда -> /start"
    )

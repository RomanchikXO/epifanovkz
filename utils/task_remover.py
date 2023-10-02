import asyncio
import schedule
import time

# Ваш список данных, который нужно очищать
my_list = [1, 2, 3, 4, 5]

def clear_list():
    global my_list
    my_list = []

async def scheduled_task():
    # Расписание выполнения задачи (каждый день в определенное время)
    schedule.every().day.at("12:00").do(clear_list)

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)  # Можете установить другой интервал, если нужно

if __name__ == "__main__":
    DataBase.create_tables()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)

    # Запуск асинхронной задачи
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_task())

    bot.infinity_polling()

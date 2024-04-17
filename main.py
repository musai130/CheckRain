from checkrain import run_selenium
import asyncio
from telegrambot import run_telegrambot
import threading


if __name__ == '__main__':
    bot_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(bot_loop)
    bot_loop.create_task(run_telegrambot())
    thread = threading.Thread(target=lambda: asyncio.run(run_selenium()))
    thread.start()
    try:
        bot_loop.run_forever()
    finally:
        bot_loop.close()
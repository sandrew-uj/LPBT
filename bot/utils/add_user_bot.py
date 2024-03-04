import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook

from config import get_webhook_url, get_webhook_path, WEBAPP_HOST, WEBHOOK_HOST, get_webapp_host
from utils.dbs.tokens import TokensDB, Token
from utils.set_bot_commands import set_default_commands
import logging


def on_startup_user_bot(user_bot, url):
    async def temp(temp_dp):
        print(f"im in set webhook url = {url}")
        await user_bot.set_webhook(url=url,
                                   # certificate=    SSL_CERTIFICATE
                                   )
        await set_default_commands(temp_dp)

    return temp


def on_shutdown_user_bot(user_bot):
    async def temp(temp_dp):
        print('Закрытие вебхука...')
        await user_bot.delete_webhook()
        await temp_dp.storage.close()
        await temp_dp.storage.wait_closed()
        print('Вебхук закрыт')
        await set_default_commands(temp_dp)

    return temp


async def add_user_bot(user_token: str):
    # print("try")
    user_bot = Bot(user_token)
    port, url = get_webhook_url()
    if user_token == "6204716568:AAGZswb927RP1rCUgDEvdyCVR27njeRicP4":
        port, url = 7001, WEBHOOK_HOST
    # dp = Dispatcher(user_bot, storage=MemoryStorage())
    url = f"{WEBHOOK_HOST}{get_webhook_path(user_token)}"

    await user_bot.set_webhook(url)

    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=get_webhook_path(user_token),
    #     on_startup=on_startup_user_bot(user_bot, url),
    #     on_shutdown=on_shutdown_user_bot(user_bot),
    #     skip_updates=True,
    #     host=get_webapp_host(user_token),
    #     port=port + 2000,
    #     # ssl_context=ssl_context
    # )

    new_token = {'token': user_token, 'port': port, 'course_id': 0}
    token = Token(**new_token)
    res = token.add()
    print(res)

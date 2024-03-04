import asyncio
from aiogram import executor, Bot
from aiogram.utils.executor import start_webhook

from config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL
from handlers import dp
from utils.add_user_bot import add_user_bot
from utils.dbs.tokens import TokensDB
# from loader import ssl_context, bot, SSL_CERTIFICATE
from utils.set_bot_commands import set_default_commands
import nest_asyncio


async def on_startup(dp):
    await set_default_commands(dp)
    tokens = TokensDB.get_all_tokens()
    for token in tokens:
        user_bot = Bot(token.token)
        webhookinfo = await user_bot.get_webhook_info()
        if not webhookinfo.url:
            print("im in not webhookinfo.url")
            await add_user_bot(token.token)
#
#
# async def on_shutdown(dp):
#     print('Закрытие вебхука...')
#     await bot.delete_webhook()
#     await dp.storage.close()
#     await dp.storage.wait_closed()
#     print('Вебхук закрыт')

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(set_default_commands(dp))
    nest_asyncio.apply()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



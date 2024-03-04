from aiogram import executor

import config
from handlers import dp
from loader import bot
from middlewares.mediagroup import AlbumMiddleware
from utils.dbs.tokens import TokensDB, Token
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    await set_default_commands(dp)
    dp.middleware.setup(AlbumMiddleware())
    token = Token(token=config.TOKEN, port=0, course_id=0)
    print(token.__dict__)
    token.add()     # ONLY FOR TESTING

    all_tokens = TokensDB.get_all_tokens()
    print(all_tokens)

    await bot.send_message(config.OWNER, text="Бот запущен!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

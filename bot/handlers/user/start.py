from aiogram import types

from loader import bot, dp
from keyboards.inline import start_kb


@dp.message_handler(commands='start', state='*')
async def starter(message: types.Message):
    await message.answer("привет, тест", reply_markup=await start_kb.get_kb(message))

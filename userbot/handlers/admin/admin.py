from aiogram import types

from keyboards.inline import admin_kb
from loader import dp


@dp.message_handler(commands='start', state='*')
async def starter(message: types.Message):
    await message.answer("Привет, выбери:", reply_markup=await admin_kb.get_kb())

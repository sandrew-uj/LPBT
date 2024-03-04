from aiogram import types, Dispatcher
from keyboards.inline import start_kb
from keyboards.inline.userbot import modules_kb


def add_start(dp: Dispatcher):
    @dp.message_handler(commands='start', state='*')
    async def starter(message: types.Message):
        await message.answer("привет, тест", reply_markup=await modules_kb.get_modules_kb(dp.bot))

from aiogram import types

import config
from FSM import FSM
from keyboards.inline.callback_datas import start_kb_callback
from loader import dp


@dp.callback_query_handler(start_kb_callback.filter(button="add_hometask"), state='*')
async def reactor(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    hometask_types = ["single", "multiple", "free_answer"]
    for hometask_type in hometask_types:
        keyboard.add(types.InlineKeyboardButton(
            text=hometask_type,
            web_app=types.WebAppInfo(url=f"{config.FRONTEND_URL}/tblp/{hometask_type}/")))

    await call.message.answer(
        "Выберите тип домашки:", reply_markup=keyboard)
    await call.answer()
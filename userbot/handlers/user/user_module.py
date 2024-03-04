from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import modules_kb, start_kb
from keyboards.inline.callback_datas import choose_module_callback
from loader import dp
from utils.send_message_with_keyboard import sender


@dp.callback_query_handler(choose_module_callback.filter(temp="arrow"), state='*')
async def reactor_arrow(call: types.CallbackQuery):
    course_id = int(choose_module_callback.parse(call.data)["course_id"])
    pos = int(choose_module_callback.parse(call.data)["pos"])
    await sender(call=call,
                 keyboard=await modules_kb.get_kb(call, course_id=course_id, pos=pos))


@dp.callback_query_handler(choose_module_callback.filter(temp="back"), state='*')
async def reactor_back(call: types.CallbackQuery, state: FSMContext):
    await sender(call, "Привет, выбери:", await start_kb.get_kb(call.message, state))


@dp.callback_query_handler(choose_module_callback.filter(temp="1"), state='*')
async def reactor_module(call: types.CallbackQuery):
    await call.answer()
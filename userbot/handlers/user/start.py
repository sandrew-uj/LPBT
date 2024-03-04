from aiogram import types
from aiogram.dispatcher import FSMContext

from FSM import FSM
from keyboards.inline.callback_datas import start_kb_callback, settings_user_callback
from loader import bot, dp
from keyboards.inline import start_kb, homeworks_kb, lessons_kb, modules_kb
from utils.dbs import homeworks
from utils.send_message_with_keyboard import sender


@dp.message_handler(commands='start', state='*')
async def starter(message: types.Message, state: FSMContext):
    await message.answer("Привет, выбери:", reply_markup=await start_kb.get_kb(message, state))


@dp.callback_query_handler(start_kb_callback.filter(button="hw"), state='*')
async def hw(call: types.CallbackQuery):
    await sender(call=call, message_text="Выбери домашку:", keyboard=await homeworks_kb.get_kb(call))


@dp.callback_query_handler(start_kb_callback.filter(button="lesson"), state='*')
async def lesson(call: types.CallbackQuery):
    await sender(call=call, message_text="Выбери урок:", keyboard=await lessons_kb.get_kb(call))


@dp.callback_query_handler(start_kb_callback.filter(button="modules"), state='*')
async def modules(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    course_id = int(data["course_id"])
    await sender(call=call, message_text="Выбери модуль:", keyboard=await modules_kb.get_kb(call, course_id))


@dp.callback_query_handler(start_kb_callback.filter(button="settings"), state='*')
async def settings(call: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Профиль", callback_data=settings_user_callback.new(button='profile')))
    await sender(call=call, message_text="Выбери настройки:", keyboard=keyboard)
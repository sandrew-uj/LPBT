from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo

from keyboards.inline import modules_kb, start_kb, admin_kb
from keyboards.inline.callback_datas import choose_module_callback, admin_kb_callback
from loader import dp
from utils.send_message_with_keyboard import sender


@dp.callback_query_handler(admin_kb_callback.filter(button="modules"), state='*')
async def module_admin(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Модули", web_app=WebAppInfo(
        url=f"www.google.com")))
    keyboard.add(types.InlineKeyboardButton(text="Управление", web_app=WebAppInfo(
        url=f"www.google.com")))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=admin_kb_callback.new(button="back")))
    await sender(call=call, message_text="Выберите действие:",
                 keyboard=keyboard)


@dp.callback_query_handler(admin_kb_callback.filter(button="back"), state='*')
async def back_to_admin(call: types.CallbackQuery):
    await sender(call, message_text="Привет, выбери:", keyboard=await admin_kb.get_kb())

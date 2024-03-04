from aiogram import types
from aiogram.types import WebAppInfo

from keyboards.inline.callback_datas import admin_kb_callback
from loader import dp
from utils.send_message_with_keyboard import sender


@dp.callback_query_handler(admin_kb_callback.filter(button="users"), state='*')
async def module_admin(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Запросы на участие", web_app=WebAppInfo(
        url=f"www.google.com")))
    keyboard.add(types.InlineKeyboardButton(text="Управление группами пользователей", web_app=WebAppInfo(
        url=f"www.google.com")))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=admin_kb_callback.new(button="back")))
    await sender(call=call, message_text="Выберите действие:",
                 keyboard=keyboard)

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo

from keyboards.inline import modules_kb, start_kb, admin_kb, access_kb, groups_kb
from keyboards.inline.callback_datas import choose_module_callback, admin_kb_callback, settings_admin_callback, \
    choose_access_callback
from keyboards.inline.start_kb import get_course
from loader import dp
from utils.send_message_with_keyboard import sender


@dp.callback_query_handler(admin_kb_callback.filter(button="settings"), state='*')
async def settings_admin(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Модель доступа", callback_data=settings_admin_callback.new(button="access")))
    keyboard.add(
        types.InlineKeyboardButton(text="Группы/каналы", callback_data=settings_admin_callback.new(button="groups")))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=admin_kb_callback.new(button="back")))
    await sender(call=call, message_text="Настройки:",
                 keyboard=keyboard)


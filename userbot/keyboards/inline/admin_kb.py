from aiogram import types
from aiogram.dispatcher import FSMContext

from FSM import FSM
from keyboards.inline.callback_datas import start_kb_callback, admin_kb_callback
from loader import bot
from utils.dbs.courses import Course, CourseDB
from utils.dbs.tokens import Token, TokensDB


async def get_kb():
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    buttons.append(types.InlineKeyboardButton(text="Модули", callback_data=admin_kb_callback.new(button="modules")))
    buttons.append(types.InlineKeyboardButton(text="Пользователи", callback_data=admin_kb_callback.new(button="users")))
    buttons.append(types.InlineKeyboardButton(text="Настройки", callback_data=admin_kb_callback.new(button="settings")))

    for button in buttons:
        keyboard.add(button)

    return keyboard

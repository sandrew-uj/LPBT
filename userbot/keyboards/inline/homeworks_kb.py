from aiogram import types
from aiogram.types import WebAppInfo

import config

from keyboards.inline.callback_datas import start_kb_callback, choose_homework_callback
from utils.dbs.homeworks import HomeworksDB


async def get_kb(call: types.CallbackQuery, pos: int = 0):
    homeworks = HomeworksDB.get_all_homeworks()

    keyboard = types.InlineKeyboardMarkup()

    for i in range(pos, pos + 5):
        if i >= len(homeworks):
            break
        homework = homeworks[i]

        title = homework.question[0:40]

        button = types.InlineKeyboardButton(text=title,
                                            callback_data=choose_homework_callback.new(homework_id=homework.homework_id,
                                                                                       pos=0,
                                                                                       temp=1))

        keyboard.add(button)

    bottom_buttons = []
    if pos > 0:
        bottom_buttons.append(types.InlineKeyboardButton(text='<',
                                                         callback_data=choose_homework_callback.new(
                                                             homework_id=0,
                                                             pos=pos - 5,
                                                             temp="arrow")))

    bottom_buttons.append(types.InlineKeyboardButton(text='назад',
                                                     callback_data=choose_homework_callback.new(
                                                         homework_id=0,
                                                         pos=0,
                                                         temp="back")))

    if pos + 5 < len(homeworks):
        bottom_buttons.append(types.InlineKeyboardButton(text='>',
                                                         callback_data=choose_homework_callback.new(
                                                             homework_id=0,
                                                             pos=pos + 5,
                                                             temp="arrow")))

    keyboard.add(*bottom_buttons)

    return keyboard

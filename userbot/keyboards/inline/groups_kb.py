from aiogram import types
from keyboards.inline.callback_datas import choose_lesson_callback, choose_group_callback
from utils.dbs.lessons import LessonDB
import json


async def get_kb(groups: str, pos: int = 0):
    groups_list = json.loads(groups)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Добавить",
                                            callback_data=choose_group_callback.new(
                                                groups=groups,
                                                group_id=0,
                                                pos=0,
                                                temp="add",
                                            )))

    for i in range(pos, pos + 5):
        if i >= len(groups_list):
            break
        group = groups_list[i]

        title = group[0:40]

        button = types.InlineKeyboardButton(text=title,
                                            callback_data=choose_group_callback.new(
                                                groups=groups,
                                                group_id=i,
                                                pos=pos,
                                                temp="chosen",
                                            ))

        keyboard.add(button)

    bottom_buttons = []
    if pos > 0:
        bottom_buttons.append(types.InlineKeyboardButton(text='<',
                                                         callback_data=choose_group_callback.new(
                                                             groups=groups,
                                                             group_id=0,
                                                             pos=pos - 5,
                                                             temp="arrow",
                                                         )))

    bottom_buttons.append(types.InlineKeyboardButton(text='назад',
                                                     callback_data=choose_group_callback.new(
                                                         groups=groups,
                                                         group_id=0,
                                                         pos=0,
                                                         temp="back",
                                                     )))

    if pos + 5 < len(groups_list):
        bottom_buttons.append(types.InlineKeyboardButton(text='>',
                                                         callback_data=choose_group_callback.new(
                                                             groups=groups,
                                                             group_id=0,
                                                             pos=pos + 5,
                                                             temp="arrow",
                                                         )))

    keyboard.add(*bottom_buttons)

    return keyboard

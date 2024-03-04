from typing import List

from aiogram import types
from aiogram.types import WebAppInfo

import config

from keyboards.inline.callback_datas import start_kb_callback, choose_homework_callback, choose_answer_callback, \
    choose_access_callback
from utils.dbs.homeworks import HomeworksDB


async def get_kb(chosen: int = 0):
    keyboard = types.InlineKeyboardMarkup()

    titles = ["ВСЕХ", "Все кто есть в группе/канале", "По телефону", "По запросу"]

    for (j, title) in zip(range(len(titles)), titles):
        text = f"{title}{'✅' if j == chosen else ''}"

        new_chosen = j
        button = types.InlineKeyboardButton(text=text,
                                            callback_data=choose_access_callback.new(
                                                temp="chosen",
                                                chosen=new_chosen,
                                            ))

        keyboard.add(button)

    keyboard.add(types.InlineKeyboardButton(text="Сохранить",
                                            callback_data=choose_access_callback.new(
                                                temp="save",
                                                chosen=chosen
                                            )))

    keyboard.add(types.InlineKeyboardButton(text="Назад",
                                            callback_data=choose_access_callback.new(
                                                temp="back",
                                                chosen=chosen
                                            )))

    return keyboard

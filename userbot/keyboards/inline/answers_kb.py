from typing import List

from aiogram import types
from aiogram.types import WebAppInfo

import config

from keyboards.inline.callback_datas import start_kb_callback, choose_homework_callback, choose_answer_callback
from utils.dbs.homeworks import HomeworksDB


async def get_kb(size: int, qtype: str, right_answers: List[int], homework_id: int, chosen: List[int] = []):
    keyboard = types.InlineKeyboardMarkup()

    for i in range(1, size + 1, 5):
        row = []
        for j in range(i, min(i + 5, size + 1)):
            title = f"{j}.{'✅' if j in chosen else ''}"

            new_chosen = [j] if qtype == 'single' else chosen + [j]

            button = types.InlineKeyboardButton(text=title,
                                                callback_data=choose_answer_callback.new(qtype=qtype,
                                                                                         chosen=new_chosen,
                                                                                         size=size,
                                                                                         right_answers=right_answers,
                                                                                         homework_id=homework_id
                                                                                         ))

            row.append(button)
        keyboard.add(*row)

    keyboard.add(types.InlineKeyboardButton(text="Сохранить ответы",
                                            callback_data=choose_answer_callback.new(qtype="save",
                                                                                     chosen=chosen,
                                                                                     size=size,
                                                                                     right_answers=right_answers,
                                                                                     homework_id=homework_id
                                                                                     )
                                            ))

    return keyboard

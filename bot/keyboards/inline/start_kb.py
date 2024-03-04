from aiogram import types
from aiogram.types import WebAppInfo

import config

from keyboards.inline.callback_datas import start_kb_callback


async def get_kb(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Подключить бота", callback_data=start_kb_callback.new(button="1"))
    button6 = types.InlineKeyboardButton(text="Создать домашку",
                                         # url=f"{config.FRONTEND_URL}/course_add/1")    #ONLY FOR TESTING)
                                         callback_data=start_kb_callback.new(button="add_hometask"))
                                         # web_app=WebAppInfo(
                                         #     url=f"{config.FRONTEND_URL}/tblp/course_add/{message.from_user.id}"))
    button2 = types.InlineKeyboardButton(text="Создать курс",
                                         # url=f"{config.FRONTEND_URL}/course_add/1")    #ONLY FOR TESTING)
                                         web_app=WebAppInfo(
                                             url=f"{config.FRONTEND_URL}/tblp/course_add/{message.from_user.id}"))

    button3 = types.InlineKeyboardButton(text="Мои курсы",
                                         web_app=WebAppInfo(
                                             url=f"{config.FRONTEND_URL}/tblp/courses/"))
    button4 = types.InlineKeyboardButton(text="Мои боты",
                                         web_app=WebAppInfo(
                                             url=f"{config.FRONTEND_URL}/tblp/bots/"))
    button5 = types.InlineKeyboardButton(text="Видеоинструкция",     callback_data=start_kb_callback.new(button="5")) # rofls

    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)
    keyboard.add(button5)
    keyboard.add(button6)

    return keyboard

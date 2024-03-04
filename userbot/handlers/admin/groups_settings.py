from aiogram import types

from FSM import FSM
from handlers.admin.admin_settings import settings_admin
from keyboards.inline import groups_kb
from keyboards.inline.callback_datas import settings_admin_callback, choose_group_callback
from keyboards.inline.start_kb import get_course
from loader import dp
from utils.send_message_with_keyboard import sender
import json


@dp.callback_query_handler(settings_admin_callback.filter(button="groups"), state='*')
async def settings_groups(call: types.CallbackQuery):
    course = get_course()
    await sender(call=call, message_text="Вот ваши группы/каналы", keyboard=await groups_kb.get_kb(course.users_group))


@dp.callback_query_handler(choose_group_callback.filter(temp="add"), state='*')
async def add_group(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text="группу",
                                      request_chat=types.KeyboardButtonRequestChat(1, chat_is_channel=False)))
    keyboard.add(types.KeyboardButton(text="канал",
                                      request_chat=types.KeyboardButtonRequestChat(1, chat_is_channel=True)))
    await sender(call=call, message_text="Выберите", keyboard=keyboard)
    await FSM.get_group_state.set()


@dp.message_handler(state=FSM.get_phone_state)
async def group_added(message: types.Message):
    chat = message.chat_shared
    await message.answer(f"Your group/channel: {chat} is added")
    course = get_course()
    groups = json.loads(course.users_group)
    groups.append(chat)
    course.users_group = json.dumps(groups)

    course.update()


@dp.callback_query_handler(choose_group_callback.filter(temp="chosen"), state='*')
async def group_chosen(call: types.CallbackQuery):
    groups = json.loads(choose_group_callback.parse(call.data)["groups"])
    group_id = int(choose_group_callback.parse(call.data)["group_id"])
    await sender(call=call, message_text=f"Выбранная группа: {groups[group_id]}")


@dp.callback_query_handler(choose_group_callback.filter(temp="arrow"), state='*')
async def group_arrow(call: types.CallbackQuery):
    groups = choose_group_callback.parse(call.data)["groups"]
    pos = int(choose_group_callback.parse(call.data)["pos"])
    await sender(call=call, message_text="Вот ваши группы/каналы",
                 keyboard=await groups_kb.get_kb(groups=groups, pos=pos))


@dp.callback_query_handler(choose_group_callback.filter(temp="back"), state='*')
async def group_back(call: types.CallbackQuery):
    await settings_admin(call)

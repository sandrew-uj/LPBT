from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo

from handlers.admin.admin_settings import settings_admin
from keyboards.inline import modules_kb, start_kb, admin_kb, access_kb, groups_kb
from keyboards.inline.callback_datas import choose_module_callback, admin_kb_callback, settings_admin_callback, \
    choose_access_callback
from keyboards.inline.start_kb import get_course
from loader import dp
from utils.send_message_with_keyboard import sender



@dp.callback_query_handler(settings_admin_callback.filter(button="access"), state='*')
async def settings_access(call: types.CallbackQuery):
    await sender(call=call, message_text="Кого допускать к курсу?",
                 keyboard=await access_kb.get_kb())


@dp.callback_query_handler(choose_access_callback.filter(temp="back"), state='*')
async def settings_access_chosen(call: types.CallbackQuery):
    await settings_admin(call)


@dp.callback_query_handler(choose_access_callback.filter(temp="chosen"), state='*')
async def settings_access_chosen(call: types.CallbackQuery):
    chosen = int(choose_access_callback.parse(call.data)["chosen"])
    await sender(call=call, message_text="Кого допускать к курсу?",
                 keyboard=await access_kb.get_kb(chosen=chosen))


@dp.callback_query_handler(choose_access_callback.filter(temp="save"), state='*')
async def settings_access_save(call: types.CallbackQuery):
    chosen = int(choose_access_callback.parse(call.data)["chosen"])
    match chosen:
        case 0:
            course_accept = "all"
        case 1:
            course_accept = "group"
        case 2:
            course_accept = "phone"
        case _:
            course_accept = "query"

    course = get_course()

    course.accept_mode = course_accept

    course.update()

    if course_accept == "group":
        await settings_groups(call)

    await call.answer("Успешно сохранено!")
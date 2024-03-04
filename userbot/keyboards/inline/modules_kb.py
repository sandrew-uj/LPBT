from aiogram import types
from keyboards.inline.callback_datas import choose_lesson_callback, choose_module_callback
from utils.dbs.courses import Course, CourseDB
from utils.dbs.lessons import LessonDB
import json

from utils.dbs.modules import Module, ModuleDB


async def get_kb(call: types.CallbackQuery, course_id: int, pos: int = 0):
    course: Course = CourseDB.get_course(course_id)

    modules = json.loads(course.modules)

    keyboard = types.InlineKeyboardMarkup()

    for i in range(pos, pos + 5):
        if i >= len(modules):
            break
        module_id = modules[i]

        module: Module = ModuleDB.get_module(module_id=module_id)

        title = module.name[0:40]

        button = types.InlineKeyboardButton(text=title,
                                            callback_data=choose_module_callback.new(module_id=module.lesson_id,
                                                                                     course_id=course_id,
                                                                                     pos=0,
                                                                                     temp=1))

        keyboard.add(button)

    bottom_buttons = []
    if pos > 0:
        bottom_buttons.append(types.InlineKeyboardButton(text='<',
                                                         callback_data=choose_module_callback.new(
                                                             module_id=0,
                                                             course_id=course_id,
                                                             pos=pos - 5,
                                                             temp="arrow")))

    bottom_buttons.append(types.InlineKeyboardButton(text='назад',
                                                     callback_data=choose_module_callback.new(
                                                         module_id=0,
                                                         course_id=course_id,
                                                         pos=0,
                                                         temp="back")))

    if pos + 5 < len(modules):
        bottom_buttons.append(types.InlineKeyboardButton(text='>',
                                                         callback_data=choose_module_callback.new(
                                                             module_id=0,
                                                             course_id=course_id,
                                                             pos=pos + 5,
                                                             temp="arrow")))

    keyboard.add(*bottom_buttons)

    return keyboard

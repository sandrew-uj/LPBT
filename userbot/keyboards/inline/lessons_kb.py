from aiogram import types
from keyboards.inline.callback_datas import choose_lesson_callback
from utils.dbs.lessons import LessonDB


async def get_kb(call: types.CallbackQuery, pos: int = 0):
    lessons = LessonDB.get_all_lessons()

    keyboard = types.InlineKeyboardMarkup()

    for i in range(pos, pos + 5):
        if i >= len(lessons):
            break
        lesson = lessons[i]

        title = lesson.name[0:40]

        button = types.InlineKeyboardButton(text=title,
                                            callback_data=choose_lesson_callback.new(lesson_id=lesson.lesson_id,
                                                                                     pos=0,
                                                                                     temp=1))

        keyboard.add(button)

    bottom_buttons = []
    if pos > 0:
        bottom_buttons.append(types.InlineKeyboardButton(text='<',
                                                         callback_data=choose_lesson_callback.new(
                                                             lesson_id=0,
                                                             pos=pos - 5,
                                                             temp="arrow")))

    bottom_buttons.append(types.InlineKeyboardButton(text='назад',
                                                     callback_data=choose_lesson_callback.new(
                                                         lesson_id=0,
                                                         pos=0,
                                                         temp="back")))

    if pos + 5 < len(lessons):
        bottom_buttons.append(types.InlineKeyboardButton(text='>',
                                                         callback_data=choose_lesson_callback.new(
                                                             lesson_id=0,
                                                             pos=pos + 5,
                                                             temp="arrow")))

    keyboard.add(*bottom_buttons)

    return keyboard

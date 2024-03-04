import json
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from FSM import FSM
from handlers.user.user_lessons import reactor_lesson
from keyboards.inline.callback_datas import start_kb_callback, choose_lesson_callback
from loader import dp
from utils.dbs.lessons import LessonDB, Lesson
from utils.send_message_with_keyboard import sender
import logging


@dp.callback_query_handler(start_kb_callback.filter(button="add_lesson"), state='*')
async def lesson_add(call: types.CallbackQuery):
    await sender(call=call, message_text="Введи название урока:")
    await FSM.type_name.set()


@dp.message_handler(state=FSM.type_name)
async def name_add(message: types.Message, state: FSMContext):
    name = message.text
    lesson_dict = LessonDB.get_default_lesson_dict()
    lesson_dict["name"] = name
    lesson = Lesson(**lesson_dict)
    await state.update_data(lesson_id=lesson.add())

    await message.answer("Отправьте единицу контента (пришлите весь контент целиком):")
    await FSM.type_content.set()


async def update_content(state: FSMContext, text: str, media_type: str, file_id):
    data = await state.get_data()
    lesson_id = data["lesson_id"]
    lesson: Lesson = LessonDB.get_lesson(lesson_id)

    content = json.loads(lesson.content)
    # print(f"content before = {content}")
    pos = len(content)
    content.append({
        "text": text,
        "media_type": media_type,
        "file_id": file_id,
        "queue": pos
    })
    # print(f"content after = {content}")

    lesson.content = json.dumps(content)

    lesson.update()


async def another_one(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Закончить", callback_data=start_kb_callback.new(button="finish")))

    await message.answer(text="Пришлите еще единицы контента, либо нажмите на кнопку закончить", reply_markup=keyboard)


@dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY, state=FSM.type_content)
async def media_group_add(message: types.Message, album: List[types.Message], state: FSMContext):
    # print("name_add")
    media_group = types.MediaGroup()
    text = ""
    num = 0
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id
        if obj.caption and obj.caption != "":
            text += f"{obj.caption}\n"

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media = {"media": file_id, "type": obj.content_type}
            # if num == 0:
            #     media["caption"] = text
            media_group.attach(media)
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")
        num += 1

    await update_content(state, text, "media_group", media_group.to_python())
    await another_one(message)

    # await message.answer_media_group(media_group)


@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.PHOTO, types.ContentType.DOCUMENT,
                                   types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE, types.ContentType.AUDIO,
                                   ], state=FSM.type_content)
async def media_add(message: types.Message, state: FSMContext):
    text = ""
    file_id = 0
    if message.text:
        text = message.text
    else:
        text = ""
        if message.photo:
            file_id = message.photo[-1].file_id
        else:
            file_id = message[message.content_type].file_id
        if message.caption and message.caption != "":
            text = message.caption

    await update_content(state, text, message.content_type, file_id)
    await another_one(message)


@dp.callback_query_handler(start_kb_callback.filter(button="finish"), state=FSM.type_content)
async def lesson_add(call: types.CallbackQuery, state: FSMContext):
    await sender(call=call, message_text="Добавление контента успешно завершено!\nВот так выглядит ваш урок:")
    data = await state.get_data()
    call.data = choose_lesson_callback.new(lesson_id=int(data["lesson_id"]),
                                           pos=0,
                                           temp=1)
    await reactor_lesson(call)
    await state.finish()

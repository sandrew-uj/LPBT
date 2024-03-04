from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.user import start
from keyboards.inline import lessons_kb, start_kb
from keyboards.inline.callback_datas import choose_lesson_callback
from loader import dp
from utils.dbs.lessons import LessonDB
from utils.send_message_with_keyboard import sender
import json


@dp.callback_query_handler(choose_lesson_callback.filter(temp="arrow"), state='*')
async def reactor_arrow(call: types.CallbackQuery):
    await sender(call=call,
                 keyboard=await lessons_kb.get_kb(call, int(choose_lesson_callback.parse(call.data)["pos"])))


@dp.callback_query_handler(choose_lesson_callback.filter(temp="back"), state='*')
async def reactor_back(call: types.CallbackQuery, state: FSMContext):
    await sender(call, "Привет, выбери:", await start_kb.get_kb(call.message, state))


@dp.callback_query_handler(choose_lesson_callback.filter(temp="1"), state='*')
async def reactor_lesson(call: types.CallbackQuery):
    await call.answer()
    lesson_id = int(choose_lesson_callback.parse(call.data)["lesson_id"])
    lesson = LessonDB.get_lesson(lesson_id)

    contents = json.loads(lesson.content)

    new_contents = sorted(contents, key=lambda d: int(d["queue"]))
    # print(contents)

    for content in new_contents:
        await get_message(call.message, content)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="удалить", callback_data=choose_lesson_callback.new(
        temp="delete",
        pos=0,
        lesson_id=lesson_id
    )))
    keyboard.add(
        types.InlineKeyboardButton(text="изменить", web_app=types.WebAppInfo(url="https://google.com")))  # rofls
    keyboard.add(types.InlineKeyboardButton(text="назад", callback_data=choose_lesson_callback.new(
        temp="back_lesson",
        pos=0,
        lesson_id=lesson_id
    )))

    await call.message.answer(text="Что вы хотите сделать с уроком? (для админов)", reply_markup=keyboard)


@dp.callback_query_handler(choose_lesson_callback.filter(temp="back_lesson"), state='*')
async def reactor_back_lesson(call: types.CallbackQuery):
    await start.lesson(call)


@dp.callback_query_handler(choose_lesson_callback.filter(temp="delete"), state='*')
async def reactor_delete_lesson(call: types.CallbackQuery):
    lesson_id = int(choose_lesson_callback.parse(call.data)["lesson_id"])
    LessonDB.delete_lesson(lesson_id)
    await sender(call=call, message_text="Успешно удалено!")


async def get_message(message: types.Message, content):
    # print(content["media_type"])
    if content["media_type"] == "text":
        await message.answer(text=content["text"])
    elif content["media_type"] == "media_group":
        media_group = types.MediaGroup()
        print(content["file_id"])

        content["file_id"][0]["caption"] = content["text"]
        for media in content["file_id"]:
            media_group.attach(media)
        await message.answer_media_group(media_group)
    elif content["media_type"] == "photo":
        await message.answer_photo(content["file_id"], caption=content["text"])
    elif content["media_type"] == "audio":
        await message.answer_audio(audio=content["file_id"], caption=content["text"])
    elif content["media_type"] == "video":
        await message.answer_video(content["file_id"], caption=content["text"])
    elif content["media_type"] == "video_note":
        await message.answer_video_note(content["file_id"])
    elif content["media_type"] == "document":
        await message.answer_document(content["file_id"], caption=content["text"])

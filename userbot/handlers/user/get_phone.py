from aiogram import types
from aiogram.dispatcher import FSMContext

from FSM import FSM
from loader import dp
from utils.dbs.courses import Course, CourseDB


@dp.message_handler(content_types=types.ContentType.CONTACT, state=FSM.get_phone_state)
async def get_user_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await message.answer(f"Твой номер успешно получен: {phone_number}",
                         reply_markup=types.ReplyKeyboardRemove())

    data = await state.get_data()
    course_id = data["course_id"]

    course: Course = CourseDB.get_course(course_id)

    is_banned = course.banned_users.__contains__(phone_number)

    if course.users.__contains__(phone_number) and not is_banned:
        await message.answer("Все отлично ты уже в базе данных курса")
    elif is_banned:
        await message.answer("Тебя забанили!")
    else:
        await message.answer("Пока тебя еще нет в базе данных курса, мы напишем админу, чтобы это исправить")

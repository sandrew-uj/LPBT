from aiogram import types
from aiogram.dispatcher import FSMContext

from FSM import FSM
from keyboards.inline.callback_datas import start_kb_callback
from loader import bot
from utils.dbs.courses import Course, CourseDB
from utils.dbs.tokens import Token, TokensDB


def get_course():
    token = bot._token

    bot_token: Token = Token(**TokensDB.get_bot(token))

    course_id = bot_token.course_id

    course: Course = CourseDB.get_course(course_id)

    return course


async def get_kb(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()

    course = get_course()

    if course.accept_mode == "phone":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Отправить номер телефона 📱", request_contact=True))
        await message.answer("Отправьте номер телефона", reply_markup=keyboard)
        await state.update_data(course_id=course.course_id)
        await FSM.get_phone_state.set()

    buttons = []
    buttons.append(types.InlineKeyboardButton(text="Модули", callback_data=start_kb_callback.new(button="modules")))
    buttons.append(types.InlineKeyboardButton(text="Настройки", callback_data=start_kb_callback.new(button="settings")))

    # button1 = types.InlineKeyboardButton(text="Показать домашки", callback_data=start_kb_callback.new(button="hw"))
    # button2 = types.InlineKeyboardButton(text="",
    #                                      # url=f"{config.FRONTEND_URL}/course_add/1")    #ONLY FOR TESTING)
    #                                      web_app=WebAppInfo(
    #                                          url=f"{config.FRONTEND_URL}/course_add/{message.from_user.id}"))
    #
    # button3 = types.InlineKeyboardButton(text="Мои курсы",
    #                                      web_app=WebAppInfo(
    #                                          url=f"{config.FRONTEND_URL}/courses/"))
    # button4 = types.InlineKeyboardButton(text="Мои боты",
    #                                      web_app=WebAppInfo(
    #                                          url=f"{config.FRONTEND_URL}/bots/"))
    # button5 = types.InlineKeyboardButton(text="Показать уроки", callback_data=start_kb_callback.new(button="lesson"))
    # button6 = types.InlineKeyboardButton(text="Добавить урок",
    #                                      callback_data=start_kb_callback.new(button="add_lesson"))

    # keyboard.add(button1)
    # keyboard.add(button2)
    # keyboard.add(button3)
    # keyboard.add(button4)
    # keyboard.add(button5)
    # keyboard.add(button6)

    for button in buttons:
        keyboard.add(button)

    return keyboard

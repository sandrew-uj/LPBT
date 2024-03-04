from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from FSM import FSM
from handlers.user import start
from keyboards.inline import homeworks_kb, answers_kb, start_kb
from keyboards.inline.callback_datas import start_kb_callback, choose_homework_callback, choose_answer_callback, \
    yes_no_callback
from loader import dp, bot
from utils.dbs.homeworks import HomeworksDB
from utils.send_message_with_keyboard import sender
import json


@dp.callback_query_handler(choose_homework_callback.filter(temp="arrow"), state='*')
async def reactor_arrow(call: types.CallbackQuery):
    await sender(call=call,
                 keyboard=await homeworks_kb.get_kb(call, int(choose_homework_callback.parse(call.data)["pos"])))


@dp.callback_query_handler(choose_homework_callback.filter(temp="back"), state='*')
async def reactor_back(call: types.CallbackQuery, state: FSMContext):
    await sender(call, "Привет, выбери:", await start_kb.get_kb(call.message, state))


@dp.callback_query_handler(choose_homework_callback.filter(temp="1"), state='*')
async def reactor(call: types.CallbackQuery, state: FSMContext):
    homework_id = int(choose_homework_callback.parse(call.data)["homework_id"])
    homework = HomeworksDB.get_homework(homework_id)

    text = f"Вопрос: {homework.question}\n"
    if homework.type != "free_answer":
        # print(homework.answers)
        # print(homework.right_answers)
        answers = json.loads(homework.answers)
        # answers = homework.answers
        idx = 1
        while answers.get(str(idx)) != None:
            text += f"{idx}. {answers[str(idx)]}\n"
            idx += 1

        right_answers = json.loads(homework.right_answers)
        await sender(call=call, message_text=text,
                     keyboard=await answers_kb.get_kb(idx - 1, homework.type, right_answers, homework_id))
    else:
        await sender(call=call, message_text=text + "Введите ответ ниже:")
        # data = {}
        # data["question"] = homework.question
        await state.update_data(question=homework.question)
        await FSM.type_answer.set()


@dp.callback_query_handler(choose_answer_callback.filter(qtype="single"), state='*')
@dp.callback_query_handler(choose_answer_callback.filter(qtype="multiple"), state='*')
async def button_pressed(call: types.CallbackQuery):
    size = int(choose_answer_callback.parse(call.data)["size"])
    homework_id = int(choose_answer_callback.parse(call.data)["homework_id"])
    qtype = choose_answer_callback.parse(call.data)["qtype"]
    chosen = json.loads(choose_answer_callback.parse(call.data)["chosen"])
    # print(chosen)
    right_answers = json.loads(choose_answer_callback.parse(call.data)["right_answers"])
    await sender(call, keyboard=await answers_kb.get_kb(size, qtype, right_answers, homework_id, chosen))


@dp.callback_query_handler(choose_answer_callback.filter(qtype="save"), state='*')
async def button_save(call: types.CallbackQuery):
    chosen = json.loads(choose_answer_callback.parse(call.data)["chosen"])
    right_answers = json.loads(choose_answer_callback.parse(call.data)["right_answers"])
    homework_id = int(choose_answer_callback.parse(call.data)["homework_id"])

    errors = 0
    for item in chosen:
        if not (item in right_answers):
            errors += 1

    errors += max(0, len(right_answers) - len(chosen))

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Попробовать еще раз",
                                            callback_data=choose_homework_callback.new(homework_id=homework_id,
                                                                                       pos=0,
                                                                                       temp=1)))

    await sender(call=call, message_text=f"{len(chosen) - errors} правильно из {len(chosen)}", keyboard=keyboard)


@dp.message_handler(state=FSM.type_answer)
async def type_answer(message: types.Message, state: FSMContext):
    answer = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    # with await state.get_data() as data:
    text = f"Ответ: {answer}\nНа вопрос: {data['question']}\nПравильно?"

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Да", callback_data=yes_no_callback.new(res="OK", student_id=user_id)))
    keyboard.add(types.InlineKeyboardButton("Нет", callback_data=yes_no_callback.new(res="Failed", student_id=user_id)))

    await bot.send_message(config.OWNER, text=text, reply_markup=keyboard)
    await message.answer("Ваш ответ отправлен на проверку модератору")
    await state.finish()


@dp.callback_query_handler(yes_no_callback.filter(res="OK"), state='*')
@dp.callback_query_handler(yes_no_callback.filter(res="Failed"), state='*')
async def yes_no(call: types.CallbackQuery, state: FSMContext):
    res = yes_no_callback.parse(call.data)["res"]
    student_id = yes_no_callback.parse(call.data)["student_id"]

    # async with state.proxy() as data:
    #     data["res"] = res
    #     data["student_id"] = student_id
    await state.update_data(res=res, student_id=student_id)
    await bot.send_message(config.OWNER, text=f"Оставьте комментарий:")
    await FSM.type_comment.set()


@dp.message_handler(state=FSM.type_comment)
async def type_comment(message: types.Message, state: FSMContext):
    comment = message.text
    data = await state.get_data()
    res = data["res"]
    student_id = data["student_id"]

    await bot.send_message(config.OWNER, text="Отправил ваш вердикт студенту!")
    await bot.send_message(student_id, text=f"Вердикт: {res}\nКомментарий:{comment}")
    await state.finish()

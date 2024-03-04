from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook

from config import get_webhook_url, get_webhook_path
from exceptions.no_available_ports import NoAvailablePorts
from loader import bot, dp
from keyboards.inline.callback_datas import start_kb_callback
from FSM import FSM
from utils.add_user_bot import add_user_bot
from utils.dbs.tokens import TokensDB


@dp.callback_query_handler(start_kb_callback.filter(button="1"), state='*')
async def reactor(call: types.CallbackQuery):
    await call.message.answer(
        "Для корректного подключения бота заранее отправьте токен, "
        "полученный у @BotFather Также необходимо войти в переписку со своим ботом и нажать 'Старт'")
    await call.message.delete()
    await FSM.add_bot_state.set()


@dp.message_handler(state=FSM.add_bot_state)
async def check_bot(message: types.Message):
    # print("check_bot")
    user_token = message.text
    try:
        await add_user_bot(user_token)
    except NoAvailablePorts:
        # print("im here")
        return await message.answer("Недостаточно портов для вебхука")
    except Exception as e:
        # print("im here")
        await message.answer(e)
        return await message.answer("Введен некорректный токен")

    return await message.answer("Бот был успешно добавлен")

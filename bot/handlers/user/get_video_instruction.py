from aiogram import types

from loader import bot, dp
from keyboards.inline.callback_datas import start_kb_callback


@dp.callback_query_handler(start_kb_callback.filter(button="5"), state='*')
async def send_instruction(call: types.CallbackQuery):
    vid = types.InputFile("permament_data/video_instruction.mp4")
    await bot.send_video(chat_id=call.from_user.id, video=vid)
    await call.message.delete()

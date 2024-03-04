from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests
import os


# Определите путь к папке, если она не существует
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Создайте бота и передайте токен
TOKEN = "6555629775:AAGaUP2nSBDq8p5ivRJ5lXCLWPM_R0dtGxY"
bot = Bot(token=TOKEN)

# Инициализируйте объект Dispatcher
dp = Dispatcher(bot)


def download_file_from_telegram(file_path, tg_id):
    bot_token = TOKEN
    
    # Создайте URL для загрузки файла с серверов Telegram
    file_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
    local_file_path = 'uploads/' + f'{tg_id}_' + file_path.split('/')[-1]

    # Определите путь к папке, если она не существует
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # Скачайте файл с серверов Telegram и сохраните его на вашем сервере
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as f:
            f.write(response.content)
        return local_file_path
    else:
        return None
    

@dp.message_handler(content_types=types.ContentType.ANY)
async def handle_media(message: types.Message):
    if message.photo:
        # Обработка фотографии
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        media_type = 'photo'
    elif message.video:
        # Обработка видео
        file_id = message.video.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        media_type = 'video'
    elif message.audio:
        # Обработка аудио
        file_id = message.audio.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        media_type = 'audio'
    elif message.voice:
        # Обработка аудио-сообщения
        file_id = message.voice.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        media_type = 'voice'

    downloaded_file_path = download_file_from_telegram(file_path, message.from_user.id)
    file_url = f'https://example.com/{downloaded_file_path}'

    await message.answer(f'Медиа-файл типа "{media_type}" получен. '
                         f'Ссылка: {file_url}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
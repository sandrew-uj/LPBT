import ssl

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# from aiogram.contrib.middlewares import logging

import config
import logging

bot = Bot(config.TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# SSL_CERTIFICATE = open("webhook_cert.pem", "rb").read()
# ssl_context.load_cert_chain("webhook_cert.pem", "webhook_pkey.pem")
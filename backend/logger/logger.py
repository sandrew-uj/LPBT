import logging
import os

# Создание экземпляра логгера
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Создание обработчика файла и установка его уровня
log_path = 'logs/app.log'
if not os.path.exists('logs'):
    os.mkdir('logs')
if not os.path.exists(log_path):
    # create a file
    with open(log_path, 'w') as fp:
        fp.write('This is first line')
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.WARNING)

# Создание обработчика консоли и установка его уровня
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Создание форматировщика и установка его для обработчиков
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Логирование сообщений
# logger.debug('Это отладочное сообщение.')
# logger.info('Это информационное сообщение.')
# logger.warning('Это предупреждающее сообщение.')
# logger.error('Это сообщение об ошибке.')
# logger.critical('Это критическое сообщение.')

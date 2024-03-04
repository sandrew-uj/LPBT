from flask import Flask, render_template, send_from_directory, jsonify, request, send_file
import requests as req
import json, os
import io
from aiogram import Bot, types, Dispatcher
from aiogram.types import InputFile

app = Flask(__name__)

REQ_URL = "http://127.0.0.1:8000"
TOKEN = "6555629775:AAGaUP2nSBDq8p5ivRJ5lXCLWPM_R0dtGxY"

bot = Bot(token=TOKEN)
title = "Опросник"
files = ['AgACAgIAAxkBAAMYZRrLtdJRUN27hpsV8-oufna1LgwAAhHQMRvNTthIAj-ThMRs_IUBAAMCAAN5AAMwBA',
         'BAACAgIAAxkBAAMaZRrOs01KxP7abBeOTO9AFN_OWYYAAvk5AALNTthIik8brBPvg-0wBA']


async def get_media_url(file_id):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    media_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    return media_url


async def get_media_info(file_id):
    file_info = await bot.get_file(file_id)
    content_type = file_info.file_path.split('.')[-1].lower()
    return content_type


def get_media_type(file_name):
    media_types = {
        'jpg': 'photo',
        'jpeg': 'photo',
        'png': 'photo',
        'gif': 'photo',
        'mp4': 'video',
        'avi': 'video',
        'mkv': 'video',
        'mp3': 'audio',
        'wav': 'audio',
    }
    return media_types.get(file_name, 'unknown')


@app.route('/tblp/editing_groups/<int:id>', methods=['GET', 'POST'])
def editing_groups(id):
    if request.method == "POST":
        print(request.get_json())

    from_list = {
        'name': 'списки',
        'list': [
            {"name": "список 1", "id": 4},
            {"name": "список 2", "id": 5},
            {"name": "список 3", "id": 6},
        ]
    }
    from_groups = {
        'name': 'группы',
        'list': [
            {"name": "группа 1", "id": 4},
            {"name": "группа 2", "id": 5},
            {"name": "группа 3", "id": 6},
        ]
    }
    from_chanal = {
        'name': 'каналы',
        'list': [
            {"name": "канал 1", "id": 1},
            {"name": "канал 2", "id": 2},
            {"name": "канал 3", "id": 3},
        ]
    }
    from_base = {
        'name': 'базы',
        'list': [
            {"name": "база 1", "id": 1},
            {"name": "база 2", "id": 2},
            {"name": "база 3", "id": 3},
        ]
    }

    inclus_lists = [from_list, from_groups, from_chanal, from_base]
    not_inclus_lists = [from_list, from_groups, from_chanal, from_base]

    content = {"inclus_lists": inclus_lists, "not_inclus_lists": not_inclus_lists, "group_id": id}
    return render_template('editing_groups.html', context=content)


@app.route('/tblp/inclus_moduls/', methods=['GET', 'POST'])
def inclus_moduls():
    if request.method == "POST":
        print(request.get_json())

    # Пример данных для таблицы
    inclus_moduls = [
        {"name": "Иванов Иван Иванович", "id": 4},
        {"name": "Петров Петр Петрович", "id": 5},
        {"name": "Сидоров Сидор Сидорович", "id": 6},
    ]

    not_inclus_moduls = [
        {"name": "Иванов Иван Иванович", "id": 1},
        {"name": "Петров Петр Петрович", "id": 2},
        {"name": "Сидоров Сидор Сидорович", "id": 3},
    ]

    content = {"inclus_moduls": inclus_moduls, "not_inclus_moduls": not_inclus_moduls}
    return render_template('inclus_moduls.html', context=content)


@app.route('/tblp/manage_groups/', methods=['GET', 'POST'])
def inclus_groups():
    if request.method == "POST":
        print(request.get_json())

    # Пример данных для таблицы
    inclus_groups = [
        {"name": "Иванов Иван Иванович", "id": 4},
        {"name": "Петров Петр Петрович", "id": 5},
        {"name": "Сидоров Сидор Сидорович", "id": 6},
    ]

    not_inclus_groups = [
        {"name": "Иванов Иван Иванович", "id": 1},
        {"name": "Петров Петр Петрович", "id": 2},
        {"name": "Сидоров Сидор Сидорович", "id": 3},
    ]

    content = {"inclus_groups": inclus_groups, "not_inclus_groups": not_inclus_groups}
    return render_template('manage_groups.html', context=content)


@app.route('/tblp/lesson_of_module/', methods=['GET', 'POST'])
def lesson_of_module():
    if request.method == "POST":
        lesson = request.get_json()
        print(lesson)

    # Пример данных для уроков
    lessons = [
        {"name": "Петров Петр Петрович"},
        {"name": "Сидоров Сидор Сидорович"},
    ]

    # Пример данных для не добавленных уроков
    new_lessons = [
        {"name": "Иванов Иван Иванович", "id": 1},
        {"name": "Петров Петр Петрович", "id": 2},
        {"name": "Сидоров Сидор Сидорович", "id": 3},
    ]

    content = {"lessons": lessons, "new_lessons": new_lessons}
    return render_template('lesson_of_module.html', context=content)


@app.route('/tblp/achieved_users/', methods=['GET', 'POST'])
def achieved_users():
    if request.method == "POST":
        # кнопка добавить
        if 'fio' in request.get_json().keys():
            user = request.get_json()  # {'fio': 'Иванов Иван Иванович'}
            print(user)

    # Пример данных для таблицы
    users = [
        {"fio": "Иванов Иван Иванович", "scores": 95, "lesson": '12122121'},
        {"fio": "Петров Петр Петрович", "scores": 80, "lesson": '32333'},
        {"fio": "Сидоров Сидор Сидорович", "scores": 70, "lesson": '3434343443'},
    ]

    content = {"users": users}
    return render_template('achieved_users.html', context=content)


@app.route('/tblp/past_users/', methods=['GET', 'POST'])
def past_users():
    if request.method == "POST":
        # кнопка добавить
        if 'fio' in request.get_json().keys():
            user = request.get_json()  # {'fio': 'Иванов Иван Иванович'}
            print(user)
        else:
            group = request.get_json()  # {'fio': 'Иванов Иван Иванович'}
            print(group)

    # Пример данных для таблицы

    groups = [
        {"name": "Группа 1"},
        {"name": "Группа 2"},
        {"name": "Группа 3"}
    ]

    users = [
        {"fio": "Иванов Иван Иванович", "scores": 95},
        {"fio": "Петров Петр Петрович", "scores": 80},
        {"fio": "Сидоров Сидор Сидорович", "scores": 70},
    ]

    content = {"users": users}
    return render_template('past_users.html', context=content)


@app.route('/tblp/admitted_users/', methods=['GET', 'POST'])
def admitted_users():
    if request.method == "POST":
        # кнопка добавить
        if 'fio' in request.get_json().keys():
            user = request.get_json()  # {'fio': 'Иванов Иван Иванович'}
            print(user)
        else:
            group = request.get_json()  # {'fio': 'Иванов Иван Иванович'}
            print(group)

    # Пример данных для таблицы

    groups = [
        {"name": "Группа 1"},
        {"name": "Группа 2"},
        {"name": "Группа 3"}
    ]

    users = [
        {"fio": "Иванов Иван Иванович", "scores": 95},
        {"fio": "Петров Петр Петрович", "scores": 80},
        {"fio": "Сидоров Сидор Сидорович", "scores": 70},
    ]

    content = {"groups": groups, "users": users}
    return render_template('admitted_users.html', context=content)


@app.route('/tblp/modul_add/', methods=['GET', 'POST'])
def modul_add():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)

    return render_template('modul_add.html')


@app.route('/tblp/lesson/', methods=['GET', 'POST'])
async def lesson():
    tg_id = '913244110'  # Замените на реальный tg_id пользователя

    if request.method == "POST":
        lesson_name = request.form.get('lesson')
        content_data = []

        for key, value in request.form.items():
            if key.startswith('content['):
                # Разбираем ключ, чтобы получить индекс и имя
                parts = key.split('][')
                index = int(parts[0].replace('content[', ''))
                field_name = parts[1].replace(']', '')

                # Если индекс больше или равен текущей длине списка content_data, добавляем новый словарь content
                while len(content_data) <= index:
                    content_data.append({})

                if field_name == 'content':
                    content_data[index][field_name] = value

                elif field_name == 'number':
                    content_data[index][field_name] = int(value)

                elif field_name == 'type':
                    content_data[index][field_name] = value

                elif field_name == 'name':
                    content_data[index][field_name] = value

        # Создаем словарь с данными урока
        lesson_data = {
            'name': lesson_name,
            'content': content_data,
            'stop_lesson': request.form.get('stop-lesson'),
            'min_points': request.form.get('min-points')
        }

        if not lesson_data['stop_lesson']:
            lesson_data['stop_lesson'] = 'on'

        lesson_json = json.dumps(lesson_data, ensure_ascii=False)
        return lesson_json

    # Перебираем файлы в папке 'uploads' и фильтруем по имени, содержащему tg_id
    media_list = []

    for file_id in files:
        content_type = await get_media_info(file_id)
        media_url = await get_media_url(file_id)
        print(content_type, media_url)
        media_list.append({'url': media_url, 'type': get_media_type(content_type)})

    print(media_list)

    content = {"title": "Урок", "media_list": media_list}
    return render_template("lesson.html", context=content)


@app.route('/tblp/single/', methods=['GET', 'POST'])
def single():
    if request.method == "POST":
        data = {"id": 0, "type": "single", "question": request.form.to_dict()['question'], "right_answers": []}
        answers = {}
        num = 0

        while True:
            num += 1
            if request.form.get(f'answers{num}') != None:
                answers[num] = request.form.get(f'answers{num}')
                if request.form.get(f'correctAnswers{num}') == "on":
                    data['right_answers'].append(num)

            else:
                data["answers"] = answers
                break

        print(data)

    content = {"title": title}
    return render_template("single_test.html", context=content)


@app.route('/tblp/multiple/', methods=['GET', 'POST'])
def multiple():
    if request.method == "POST":
        print(request.form.to_dict())
        data = {"id": 0, "type": "multiple", "question": request.form.to_dict()['question'], "right_answers": []}
        answers = {}
        num = 0

        while True:
            num += 1
            if request.form.get(f'answers{num}') != None:
                answers[num] = request.form.get(f'answers{num}')
                print(request.form.get(f'correctAnswers{num}'), request.form.get(f'answers{num}'))
                if request.form.get(f'correctAnswers{num}') == "on":
                    data['right_answers'].append(num)

            else:
                data["answers"] = answers
                break

        print(data)

    content = {"title": title}
    return render_template("multiple_test.html", context=content)


@app.route('/tblp/free_answer/', methods=['GET', 'POST'])
def free_answer():
    if request.method == "POST":
        data = {"id": 0, "type": "free_answer", "question": request.form.to_dict()['question'], "right_answers": [],
                "answers": []}
        print(data)

    content = {"title": title}
    return render_template("free_answer.html", context=content)


async def cmd_start(message: types.Message):
    await message.answer("hello")


@app.route('/tblp/<token>', methods=['GET', 'POST'])
def bot_webhook(token):
    update = request.get_json()
    telegram_update = types.Update(**update)
    bot = Bot(token)
    dp = Dispatcher(bot)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.process_update(telegram_update)

    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)

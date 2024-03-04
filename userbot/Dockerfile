FROM python:3.10

RUN apt update -y

ADD ./ /userbot/

WORKDIR /userbot

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]


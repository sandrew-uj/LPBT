FROM python:3.10

RUN apt update -y

ADD ./ /backend/

WORKDIR /backend

RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


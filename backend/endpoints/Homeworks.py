from fastapi import FastAPI

from Models.homework import Homework, HomeworkDB

app_homework = FastAPI(
    title="backend_homework"
)


@app_homework.post("/add_homework")
def add_homework(homework: Homework):
    homework.add_homework()


@app_homework.get("/get_all_homeworks")
def get_all_homeworks():
    return HomeworkDB.get_homeworks()
    # homework.add_homework()


@app_homework.get("/get_homework/{homework_id}")
def get_homework(homework_id: int):
    return HomeworkDB.get_homework(homework_id)
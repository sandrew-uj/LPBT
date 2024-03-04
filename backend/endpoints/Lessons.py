from fastapi import FastAPI
from Models.lesson import Lesson, LessonDB

app_lesson = FastAPI(
    title="backend_lesson"
)


@app_lesson.post("/add_lesson")
async def add_lesson(lesson: Lesson) -> int:
    lesson_id = lesson.add_lesson()
    return lesson_id


@app_lesson.get("/get_all_lessons")
async def get_all_lessons():
    lessons = LessonDB.get_lessons()
    return lessons


@app_lesson.get("/get_lesson/{lesson_id}")
async def get_lesson(lesson_id: int):
    lesson = LessonDB.get_lesson_by_id(lesson_id)
    if lesson:
        return lesson
    return None


@app_lesson.post("/update_lesson/")
def update_lesson(lesson: Lesson):
    # lesson.lesson_id = lesson_id
    # lesson = LessonDB.get_lesson_by_id(lesson.lesson_id)
    lesson.update_lesson()
    return {"message": "Lesson updated successfully"}


@app_lesson.get("/delete_lesson/{lesson_id}")
def delete_lesson(lesson_id: int):
    LessonDB.delete_lesson(lesson_id)
    return {"message": "Lesson deleted successfully"}

from typing import List

import requests
from pydantic import BaseModel

import config
import json


class Lesson(BaseModel):
    lesson_id: int
    course_id: int
    module_id: int
    name: str
    homeworks: str  # json line list of int
    content: str  # json line list of jsons
    reached_users: str  # json line list of int
    passed_users: str  # json line list of int
    stop_lesson: bool
    min_points: int

    def add(self) -> int:
        return LessonDB.add_lesson(self)

    def update(self):
        return LessonDB.update_lesson(self)


class LessonDB:

    @staticmethod
    def add_lesson(lesson: Lesson) -> int:
        res = requests.post(f"{config.BACKEND_URL}/tblp/lessons/add_lesson", json.dumps(lesson.__dict__))
        return int(res.json())

    @staticmethod
    def update_lesson(lesson: Lesson):
        res = requests.post(f"{config.BACKEND_URL}/tblp/lessons/update_lesson", json.dumps(lesson.__dict__))
        return res

    @staticmethod
    def delete_lesson(lesson_id: int):
        res = requests.get(f"{config.BACKEND_URL}/tblp/lessons/delete_lesson/{lesson_id}")
        return res


    @staticmethod
    def get_lesson(lesson_id: int) -> Lesson | None:
        res = requests.get(f"{config.BACKEND_URL}/tblp/lessons/get_lesson/{lesson_id}")
        if res.json() == "None":
            return None
        return Lesson(**res.json())

    @staticmethod
    def get_all_lessons() -> List[Lesson]:
        res = requests.get(f"{config.BACKEND_URL}/tblp/lessons/get_all_lessons")
        ans = []
        for i in res.json():
            ans.append(Lesson(**i))
        return ans

    @staticmethod
    def get_default_lesson_dict():
        return {
            "lesson_id": 0,
            "course_id": 0,
            "module_id": 0,
            "name": "",
            "homeworks": "[]",
            "content": "[]",
            "reached_users": "[]",
            "passed_users": "[]",
            "stop_lesson": False,
            "min_points": 0
        }

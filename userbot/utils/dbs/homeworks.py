from typing import List

import requests
from pydantic import BaseModel

import config


class Homework(BaseModel):
    homework_id: int
    course_id: int
    module_id: int
    lesson_id: int
    type: str
    question: str
    answers: str
    right_answers: str

    # def add(self):
    #     return HomeworksDB.add_h(self)


class HomeworksDB:

    @staticmethod
    def get_homework(homework_id: int):
        res = requests.get(f"{config.BACKEND_URL}/tblp/homeworks/get_homework/{homework_id}")
        if res.json() == "None":
            return None
        return Homework(**res.json())

    @staticmethod
    def get_all_homeworks() -> List[Homework]:
        res = requests.get(f"{config.BACKEND_URL}/tblp/homeworks/get_all_homeworks")
        ans = []
        for i in res.json():
            ans.append(Homework(**i))
        return ans

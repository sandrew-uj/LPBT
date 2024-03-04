from typing import List

import requests
from pydantic import BaseModel
import config
import json


class Course(BaseModel):
    course_id: int
    bot_id: int
    name: str
    modules: str
    users: str
    accepted_users: str
    banned_users: str
    passed_users: str
    users_group: str
    accept_mode: str
    settings: str

    def add(self) -> int:
        return CourseDB.add_course(self)

    def update(self):
        return CourseDB.update_course(self)


class CourseDB:

    @staticmethod
    def add_course(course: Course) -> int:
        res = requests.post(f"{config.BACKEND_URL}/tblp/courses/add_course", json.dumps(course.__dict__))
        return int(res.json())

    @staticmethod
    def update_course(course: Course):
        res = requests.post(f"{config.BACKEND_URL}/tblp/courses/update_course", json.dumps(course.__dict__))
        return res

    @staticmethod
    def delete_course(course_id: int):
        res = requests.get(f"{config.BACKEND_URL}/tblp/courses/delete_course/{course_id}")
        return res

    @staticmethod
    def get_course(course_id: int) -> Course | None:
        res = requests.get(f"{config.BACKEND_URL}/tblp/courses/get_course/{course_id}")
        if res.json() == "None":
            return None
        return Course(**res.json())

    @staticmethod
    def get_all_courses() -> List[Course]:
        res = requests.get(f"{config.BACKEND_URL}/tblp/courses/get_all_courses")
        ans = []
        for i in res.json():
            ans.append(Course(**i))
        return ans

    # @staticmethod
    # def get_modules_by

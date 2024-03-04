from typing import List

import requests
from pydantic import BaseModel
import config
import json


class Module(BaseModel):
    module_id: int
    course_id: int
    name: str
    description: str
    lessons: str
    reached_users: str
    passed_users: str
    accepted_users: str

    # def add(self) -> int:
    #     return CourseDB.add_course(self)
    #
    # def update(self):
    #     return CourseDB.update_course(self)


class ModuleDB:

    # @staticmethod
    # def add_course(course: Course) -> int:
    #     res = requests.post(f"{config.BACKEND_URL}/tblp/courses/add_course", json.dumps(course.__dict__))
    #     return int(res.json())
    #
    # @staticmethod
    # def update_course(course: Course):
    #     res = requests.post(f"{config.BACKEND_URL}/tblp/courses/update_course", json.dumps(course.__dict__))
    #     return res

    # @staticmethod
    # def delete_course(course_id: int):
    #     res = requests.get(f"{config.BACKEND_URL}/tblp/courses/delete_course/{course_id}")
    #     return res
    #
    @staticmethod
    def get_module(module_id: int) -> Module | None:
        res = requests.get(f"{config.BACKEND_URL}/tblp/courses/get_course/{module_id}")
        if res.json() == "None":
            return None
        return Module(**res.json())

    # @staticmethod
    # def get_modules_by() -> List[Course]:
    #     res = requests.get(f"{config.BACKEND_URL}/tblp/courses/get_all_courses")
    #     ans = []
    #     for i in res.json():
    #         ans.append(Course(**i))
    #     return ans

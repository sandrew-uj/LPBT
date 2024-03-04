from fastapi import FastAPI
from Models.course import Course, CourseDB  # Assuming you have a Course model and CourseDB class

app_course = FastAPI(
    title="backend_course"
)


@app_course.post("/add_course")
async def add_course(course: Course) -> int:
    course_id = course.add_course()
    return course_id


@app_course.get("/get_all_courses")
async def get_all_courses():
    courses = CourseDB.get_courses()
    return courses


@app_course.get("/get_course/{course_id}")
async def get_course(course_id: int):
    course = CourseDB.get_course_by_id(course_id)
    if course:
        return course
    return None


@app_course.post("/update_course")
def update_course(course: Course):
    course.update_course()
    return {"message": "Course updated successfully"}


@app_course.get("/delete_course/{course_id}")
def delete_course(course_id: int):
    CourseDB.delete_course(course_id)
    return {"message": "Course deleted successfully"}

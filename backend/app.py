from fastapi import FastAPI

from endpoints.Admins import app_admin
from endpoints.Courses import app_course
from endpoints.Homeworks import app_homework
from endpoints.Lessons import app_lesson
from endpoints.Tokens import app_token
from endpoints.Users import app_user
from logger.logger import logger

app = FastAPI(
    title="TBLP_backend"
)

app.mount("/tblp/tokens/", app_token)
app.mount("/tblp/homeworks/", app_homework)
app.mount("/tblp/lessons/", app_lesson)
app.mount("/tblp/courses/", app_course)
app.mount("/tblp/admins/", app_admin)
app.mount("/tblp/users/", app_user)

logger.info("program_started")

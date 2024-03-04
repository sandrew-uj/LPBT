import os
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLite database engine
if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/Homework.db', echo=False)

Base = declarative_base()


# Define the Homework model
class Homework(BaseModel):
    homework_id: int
    course_id: int
    module_id: int
    lesson_id: int
    type: str
    question: str
    answers: str
    right_answers: str

    def add_homework(self) -> int:
        return HomeworkDB.add_homework(self)


# Create the Homework table in the database
class HomeworkModel(Base):
    __tablename__ = 'Homework'
    homework_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer)
    module_id = Column(Integer)
    lesson_id = Column(Integer)
    type = Column(String)
    question = Column(String)
    answers = Column(String)
    right_answers = Column(String)

    def __repr__(self):
        return (f"homework_id={self.homework_id}, course_id={self.course_id}, module_id={self.module_id},"
                f" lesson_id={self.lesson_id}, type='{self.type}'")


# Create the table if it doesn't exist
inspector = inspect(engine)
if not inspector.has_table(HomeworkModel.__tablename__):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# Define a class to interact with the Homework table
class HomeworkDB:
    @staticmethod
    def add_homework(homework: Homework) -> int:
        """
        Add a new homework entry.

        Args:
            homework (Homework): Homework object with all required fields.

        Returns:
            int: The ID of the newly added homework entry.
        """
        new_homework = HomeworkModel(
            course_id=homework.course_id,
            module_id=homework.module_id,
            lesson_id=homework.lesson_id,
            type=homework.type,
            question=homework.question,
            answers=homework.answers,
            right_answers=homework.right_answers
        )
        session.add(new_homework)
        session.commit()
        return new_homework.homework_id

    @staticmethod
    def get_homeworks():
        return session.query(HomeworkModel).all()

    @staticmethod
    def get_homework(homework_id: int):
        return session.query(HomeworkModel).filter_by(homework_id=homework_id).first()

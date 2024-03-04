import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic import BaseModel
from typing_extensions import List

if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/Lesson.db', echo=False)

Base = declarative_base()


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

    def add_lesson(self) -> int:
        """
        Add a new lesson.

        Returns:
            int: The ID of the newly added lesson.
        """
        return LessonDB.add_lesson(self)

    def update_lesson(self) -> None:
        """
        Update the lesson's data in the database.

        Returns:
            None
        """
        LessonDB.update_lesson(self)

    def delete_lesson(self) -> None:
        """
        Delete the lesson from the database.

        Returns:
            None
        """
        LessonDB.delete_lesson(self.lesson_id)


class LessonModel(Base):
    __tablename__ = 'Lesson'
    lesson_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer)
    module_id = Column(Integer)
    name = Column(String)
    homeworks = Column(String)
    content = Column(String)
    reached_users = Column(String)
    passed_users = Column(String)
    stop_lesson = Column(Boolean)
    min_points = Column(Integer)

    def __repr__(self):
        return (f"lesson_id={self.lesson_id}, course_id={self.course_id}, module_id={self.module_id}, "
                f"name='{self.name}', homeworks='{self.homeworks}', content='{self.content}', "
                f"reached_users='{self.reached_users}', passed_users='{self.passed_users}', "
                f"stop_lesson={self.stop_lesson}, min_points={self.min_points}")


# Rest of the code remains the same.


# Create the table if it doesn't exist
inspector = inspect(engine)
if not inspector.has_table(LessonModel.__tablename__):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class LessonDB:
    @staticmethod
    def add_lesson(lesson: Lesson) -> int:
        """
        Add a new lesson to the database.

        Args:
            lesson (Lesson): The Lesson object to add.

        Returns:
            int: The ID of the newly added lesson.
        """
        new_lesson = LessonModel(
            course_id=lesson.course_id,
            module_id=lesson.module_id,
            name=lesson.name,
            homeworks=lesson.homeworks,
            content=lesson.content,
            reached_users=lesson.reached_users,
            passed_users=lesson.passed_users,
            stop_lesson=lesson.stop_lesson,
            min_points=lesson.min_points
        )
        session.add(new_lesson)
        session.commit()
        return new_lesson.lesson_id

    @staticmethod
    def get_lesson_by_id(lesson_id: int) -> Lesson:
        """
        Get a lesson by its ID.

        Args:
            lesson_id (int): The ID of the lesson to retrieve.

        Returns:
            Lesson: The lesson object.
        """
        lesson_model = session.query(LessonModel).filter_by(lesson_id=lesson_id).first()
        if lesson_model:
            return Lesson(
                lesson_id=lesson_model.lesson_id,
                course_id=lesson_model.course_id,
                module_id=lesson_model.module_id,
                name=lesson_model.name,
                homeworks=lesson_model.homeworks,
                content=lesson_model.content,
                reached_users=lesson_model.reached_users,
                passed_users=lesson_model.passed_users,
                stop_lesson=lesson_model.stop_lesson,
                min_points=lesson_model.min_points
            )
        return None

    @staticmethod
    def update_lesson(lesson: Lesson) -> None:
        """
        Update a lesson's data by its ID.

        Args:
            lesson (Lesson): The Lesson object with updated data.
        """

        print(lesson)

        lesson_model = session.query(LessonModel).filter_by(lesson_id=lesson.lesson_id).first()
        if lesson_model:
            lesson_model.course_id = lesson.course_id
            lesson_model.module_id = lesson.module_id
            lesson_model.name = lesson.name
            lesson_model.homeworks = lesson.homeworks
            lesson_model.content = lesson.content
            lesson_model.reached_users = lesson.reached_users
            lesson_model.passed_users = lesson.passed_users
            lesson_model.stop_lesson = lesson.stop_lesson
            lesson_model.min_points = lesson.min_points
            session.commit()

    @staticmethod
    def delete_lesson(lesson_id: int) -> None:
        """
        Delete a lesson by its ID.

        Args:
            lesson_id (int): The ID of the lesson to delete.
        """
        lesson_model = session.query(LessonModel).filter_by(lesson_id=lesson_id).first()
        if lesson_model:
            session.delete(lesson_model)
            session.commit()

    @staticmethod
    def get_lessons():
        return session.query(LessonModel).all()

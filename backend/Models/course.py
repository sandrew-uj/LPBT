import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/Course.db', echo=False)

Base = declarative_base()


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

    def add_course(self) -> int:
        """
        Add a new course.

        Returns:
            int: The ID of the newly added course.
        """
        return CourseDB.add_course(self)

    def update_course(self) -> None:
        """
        Update the course's data in the database.

        Returns:
            None
        """
        CourseDB.update_course(self)

    def delete_course(self) -> None:
        """
        Delete the course from the database.

        Returns:
            None
        """
        CourseDB.delete_course(self.course_id)


class CourseModel(Base):
    __tablename__ = 'Course'
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    bot_id = Column(Integer)
    name = Column(String)
    modules = Column(String)
    users = Column(String)
    accepted_users = Column(String)
    banned_users = Column(String)
    passed_users = Column(String)
    users_group = Column(String)
    accept_mode = Column(String)
    settings = Column(String)

    def __repr__(self):
        return (
            f"course_id={self.course_id}, bot_id={self.bot_id}, name='{self.name}', modules='{self.modules}', "
            f"users='{self.users}', accepted_users='{self.accepted_users}', banned_users='{self.banned_users}', "
            f"passed_users='{self.passed_users}', users_group='{self.users_group}', "
            f"accept_mode='{self.accept_mode}', settings='{self.settings}'"
        )


# Rest of the code remains the same.

# Create the table if it doesn't exist
inspector = inspect(engine)
if not inspector.has_table(CourseModel.__tablename__):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class CourseDB:
    @staticmethod
    def add_course(course: Course) -> int:
        """
        Add a new course to the database.

        Args:
            course (Course): The Course object to add.

        Returns:
            int: The ID of the newly added course.
        """
        new_course = CourseModel(
            bot_id=course.bot_id,
            name=course.name,
            modules=course.modules,
            users=course.users,
            accepted_users=course.accepted_users,
            banned_users=course.banned_users,
            passed_users=course.passed_users,
            users_group=course.users_group,
            accept_mode=course.accept_mode,
            settings=course.settings
        )
        session.add(new_course)
        session.commit()
        return new_course.course_id

    @staticmethod
    def get_course_by_id(course_id: int) -> Course:
        """
        Get a course by its ID.

        Args:
            course_id (int): The ID of the course to retrieve.

        Returns:
            Course: The course object.
        """
        course_model = session.query(CourseModel).filter_by(course_id=course_id).first()
        if course_model:
            return Course(
                course_id=course_model.course_id,
                bot_id=course_model.bot_id,
                name=course_model.name,
                modules=course_model.modules,
                users=course_model.users,
                accepted_users=course_model.accepted_users,
                banned_users=course_model.banned_users,
                passed_users=course_model.passed_users,
                users_group=course_model.users_group,
                accept_mode=course_model.accept_mode,
                settings=course_model.settings
            )
        return None

    @staticmethod
    def update_course(course: Course) -> None:
        """
        Update a course's data by its ID.

        Args:
            course (Course): The Course object with updated data.
        """

        course_model = session.query(CourseModel).filter_by(course_id=course.course_id).first()
        if course_model:
            course_model.bot_id = course.bot_id
            course_model.name = course.name
            course_model.modules = course.modules
            course_model.users = course.users
            course_model.accepted_users = course.accepted_users
            course_model.banned_users = course.banned_users
            course_model.passed_users = course.passed_users
            course_model.users_group = course.users_group
            course_model.accept_mode = course.accept_mode
            course_model.settings = course.settings
            session.commit()

    @staticmethod
    def delete_course(course_id: int) -> None:
        """
        Delete a course by its ID.

        Args:
            course_id (int): The ID of the course to delete.
        """
        course_model = session.query(CourseModel).filter_by(course_id=course_id).first()
        if course_model:
            session.delete(course_model)
            session.commit()

    @staticmethod
    def get_courses():
        return session.query(CourseModel).all()

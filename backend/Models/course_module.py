from pydantic import BaseModel

import os
from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/CourseModule.db', echo=False)

Base = declarative_base()


class CourseModule(BaseModel):
    record_id: int
    course_id: int
    module_id: int

    async def add_course_module(self) -> int:
        return await CourseModuleDb.add_course_module(self)


class CourseModuleModel(Base):
    __tablename__ = 'CourseModule'
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer)
    module_id = Column(Integer)

    def __repr__(self):
        return f"record_id={self.record_id}, course_id={self.course_id}, module_id={self.module_id}"


# Create the table if it doesn't exist
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class CourseModuleDb:
    @staticmethod
    async def add_course_module(course_module: CourseModule) -> int:
        """
        Add a new course-module relationship.

        Args:
            course_module (CourseModule): CourseModule object with record_id, course_id, and module_id.

        Returns:
            int: The ID of the newly added course-module relationship.
        """
        new_course_module = CourseModuleModel(
            course_id=course_module.course_id,
            module_id=course_module.module_id
        )
        session.add(new_course_module)
        session.commit()
        return new_course_module.record_id


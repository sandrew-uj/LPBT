from pydantic import BaseModel
import os
from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/ModuleLesson.db', echo=False)

Base = declarative_base()


class ModuleLesson(BaseModel):
    record_id: int
    module_id: int
    lesson_id: int

    async def add_module_lesson(self) -> int:
        return await ModuleLessonDb.add_module_lesson(self)


class ModuleLessonModel(Base):
    __tablename__ = 'ModuleLesson'
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey('Module.module_id'))
    lesson_id = Column(Integer, ForeignKey('Lesson.lesson_id'))

    def __repr__(self):
        return f"record_id={self.record_id}, module_id={self.module_id}, lesson_id={self.lesson_id}"


# Create the table if it doesn't exist
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class ModuleLessonDb:
    @staticmethod
    async def add_module_lesson(module_lesson: ModuleLesson) -> int:
        """
        Add a new module-lesson relationship.

        Args:
            module_lesson (ModuleLesson): ModuleLesson object with record_id, module_id, and lesson_id.

        Returns:
            int: The ID of the newly added module-lesson relationship.
        """
        new_module_lesson = ModuleLessonModel(
            module_id=module_lesson.module_id,
            lesson_id=module_lesson.lesson_id
        )
        session.add(new_module_lesson)
        session.commit()
        return new_module_lesson.record_id

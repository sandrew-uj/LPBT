import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic import BaseModel
from typing_extensions import List

if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/Module.db', echo=False)

Base = declarative_base()


class Module(BaseModel):
    module_id: int
    course_id: int
    name: str
    description: str
    lessons: str
    reached_users: str
    passed_users: str
    accepted_users: str

    def add_module(self) -> int:
        """
        Add a new module.

        Returns:
            int: The ID of the newly added module.
        """
        return ModuleDB.add_module(self)

    def update_module(self) -> None:
        """
        Update the module's data in the database.

        Returns:
            None
        """
        ModuleDB.update_module(self)

    def delete_module(self) -> None:
        """
        Delete the module from the database.

        Returns:
            None
        """
        ModuleDB.delete_module(self.module_id)


class ModuleModel(Base):
    __tablename__ = 'Module'
    module_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    lessons = Column(String)
    reached_users = Column(String)
    passed_users = Column(String)
    accepted_users = Column(String)

    def __repr__(self):
        return (f"module_id={self.module_id}, course_id={self.course_id}, "
                f"name='{self.name}', description='{self.description}', "
                f"lessons='{self.lessons}', reached_users='{self.reached_users}', "
                f"passed_users='{self.passed_users}', accepted_users='{self.accepted_users}'")


# Rest of the code remains the same.

# Create the table if it doesn't exist
inspector = inspect(engine)
if not inspector.has_table(ModuleModel.__tablename__):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class ModuleDB:
    @staticmethod
    def add_module(module: Module) -> int:
        """
        Add a new module to the database.

        Args:
            module (Module): The Module object to add.

        Returns:
            int: The ID of the newly added module.
        """
        new_module = ModuleModel(
            course_id=module.course_id,
            name=module.name,
            description=module.description,
            lessons=module.lessons,
            reached_users=module.reached_users,
            passed_users=module.passed_users,
            accepted_users=module.accepted_users
        )
        session.add(new_module)
        session.commit()
        return new_module.module_id

    @staticmethod
    def get_module_by_id(module_id: int) -> Module:
        """
        Get a module by its ID.

        Args:
            module_id (int): The ID of the module to retrieve.

        Returns:
            Module: The module object.
        """
        module_model = session.query(ModuleModel).filter_by(module_id=module_id).first()
        if module_model:
            return Module(
                module_id=module_model.module_id,
                course_id=module_model.course_id,
                name=module_model.name,
                description=module_model.description,
                lessons=module_model.lessons,
                reached_users=module_model.reached_users,
                passed_users=module_model.passed_users,
                accepted_users=module_model.accepted_users
            )
        return None

    @staticmethod
    def update_module(module: Module) -> None:
        """
        Update a module's data by its ID.

        Args:
            module (Module): The Module object with updated data.
        """
        module_model = session.query(ModuleModel).filter_by(module_id=module.module_id).first()
        if module_model:
            module_model.course_id = module.course_id
            module_model.name = module.name
            module_model.description = module.description
            module_model.lessons = module.lessons
            module_model.reached_users = module.reached_users
            module_model.passed_users = module.passed_users
            module_model.accepted_users = module.accepted_users
            session.commit()

    @staticmethod
    def delete_module(module_id: int) -> None:
        """
        Delete a module by its ID.

        Args:
            module_id (int): The ID of the module to delete.
        """
        module_model = session.query(ModuleModel).filter_by(module_id=module_id).first()
        if module_model:
            session.delete(module_model)
            session.commit()

    @staticmethod
    def get_modules():
        return session.query(ModuleModel).all()


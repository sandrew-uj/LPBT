import os
from typing import List, Any
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Admin(BaseModel):
    name: str
    surname: str
    profile_pic: bytes  # You can use bytes or str to represent the profile picture
    # add users list
    # add channels
    # add bases
    groups: str
    courses: str
    modules: str


if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/Admin.db', echo=False)

Base = declarative_base()


class AdminModel(Base):
    __tablename__ = 'Admin'
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    profile_pic = Column(LargeBinary)  # Store profile_pic as bytes
    groups = Column(String)
    courses = Column(String)
    modules = Column(String)

    def __repr__(self):
        return f"name='{self.name}', surname='{self.surname}', profile_pic='{self.profile_pic}', " \
               f"groups='{self.groups}', courses='{self.courses}', modules='{self.modules}')"


# Create the table if it doesn't exist
inspector = inspect(engine)
if not inspector.has_table(AdminModel.__tablename__):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class AdminDB:
    @staticmethod
    async def add_admin(admin: dict) -> int:
        """
        Add a new admin to the database.

        Args:
            admin (dict): Admin information, including 'name', 'surname', 'profile_pic', 'groups', 'courses', and 'modules'.

        Returns:
            int: Admin ID of the newly added admin.
        """
        new_admin = AdminModel(name=admin['name'], surname=admin['surname'], profile_pic=admin['profile_pic'],
                               groups=admin['groups'], courses=admin['courses'], modules=admin['modules'])
        session.add(new_admin)
        session.commit()
        return new_admin.admin_id

    @staticmethod
    async def get_admin_by_id(admin_id: int):
        """
        Get an admin by admin_id.

        Args:
            admin_id (int): Admin ID.

        Returns:
            AdminModel: Admin model object or None if not found.
        """
        admin = session.query(AdminModel).filter_by(admin_id=admin_id).first()
        return admin

    @staticmethod
    async def get_all_admins():
        """
        Get all admins from the Admin table.

        Returns:
            List[AdminModel]: List of admin model objects.
        """
        return session.query(AdminModel).all()

    @staticmethod
    async def get_admin_courses(admin_id: int):
        """
        Get the 'courses' field for an admin by admin_id.

        Args:
            admin_id (int): Admin ID.

        Returns:
            str: Admin's courses or None if not found.
        """
        admin = session.query(AdminModel.courses).filter_by(admin_id=admin_id).first()
        return admin[0] if admin else None

    @staticmethod
    async def get_admin_modules(admin_id: int):
        """
        Get the 'modules' field for an admin by admin_id.

        Args:
            admin_id (int): Admin ID.

        Returns:
            str: Admin's modules or None if not found.
        """
        admin = session.query(AdminModel.modules).filter_by(admin_id=admin_id).first()
        return admin[0] if admin else None

    @staticmethod
    async def get_admin_groups(admin_id: int):
        """
        Get the 'groups' field for an admin by admin_id.

        Args:
            admin_id (int): Admin ID.

        Returns:
            str: Admin's groups or None if not found.
        """
        admin = session.query(AdminModel.groups).filter_by(admin_id=admin_id).first()
        return admin[0] if admin else None

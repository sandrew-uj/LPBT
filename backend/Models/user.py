import os
from typing import List, Any
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class User(BaseModel):
    name: str
    surname: str
    profile_pic: bytes  # You can use bytes or str to represent the profile picture


if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/User.db', echo=False)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    profile_pic = Column(LargeBinary)  # Store profile_pic as bytes

    def __repr__(self):
        return f"name='{self.name}', surname='{self.surname}', profile_pic='{self.profile_pic}')"


# Create the table if it doesn't exist
inspector = inspect(engine)
if not inspector.has_table(UserModel.__tablename__):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class UserDB:
    @staticmethod
    async def add_user(user: dict) -> int:
        """
        Add a new user to the database.

        Args:
            user (dict): User information, including 'name', 'surname', and 'profile_pic'.

        Returns:
            int: User ID of the newly added user.
        """
        new_user = UserModel(name=user['name'], surname=user['surname'], profile_pic=user['profile_pic'])
        session.add(new_user)
        session.commit()
        return new_user.user_id

    @staticmethod
    async def get_user_by_id(user_id: int):
        """
        Get a user by user_id.

        Args:
            user_id (int): User ID.

        Returns:
            UserModel: User model object or None if not found.
        """
        user = session.query(UserModel).filter_by(user_id=user_id).first()
        return user

    @staticmethod
    async def get_all_users():
        """
        Get all users from the User table.

        Returns:
            List[UserModel]: List of user model objects.
        """
        return session.query(UserModel).all()

    @staticmethod
    async def get_user_by_name_surname(name: str, surname: str):
        """
        Get a user by name and surname.

        Args:
            name (str): User's name.
            surname (str): User's surname.

        Returns:
            UserModel: User model object or None if not found.
        """
        user = session.query(UserModel).filter_by(name=name, surname=surname).first()
        return user

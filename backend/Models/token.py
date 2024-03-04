import os
from typing import Type, List, Any

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Token(BaseModel):
    token: str
    port: int
    course_id: int

    async def add_token(self) -> int:
        return await TokenDB.add_token(self)


if not os.path.exists('dbs'):
    os.makedirs('dbs')

engine = create_engine('sqlite:///dbs/Token.db', echo=False)

Base = declarative_base()


class TokenModel(Base):
    __tablename__ = 'Token'
    token_id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String)
    port = Column(Integer)
    course_id = Column(Integer)

    def __repr__(self):
        return f"token='{self.token}', " \
               f")"


# Create the table if it doesn't exist
inspector = inspect(engine)
if not inspector.has_table(TokenModel.__tablename__):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class TokenDB:

    @staticmethod
    async def add_token(token: Token) -> int:
        """
        Add a new token.

        Args:
            token (str): Name of the token.

        Returns:
            None
        """
        new_token = TokenModel(token=token.token, port=token.port, course_id=token.course_id)
        session.add(new_token)
        session.commit()
        return new_token.token_id

    @staticmethod
    async def get_ports() -> List[int]:
        """
        Get all used ports in tokens.

        Args:
            None

        Returns:
            List of used ports
        """
        ports = session.query(TokenModel.port).all()
        session.commit()
        return ports

    @staticmethod
    async def get_token(**kwargs: Any):
        """
        get token by kwargs.

        Args:
            kwargs dict[str, Any]: kwargs to filter tokens.

        Returns:
            None
        """

        return session.query(TokenModel.token, TokenModel.port, TokenModel.course_id).filter_by(**kwargs).first()

    @staticmethod
    async def get_all_tokens():
        return session.query(TokenModel.token, TokenModel.port, TokenModel.course_id).all()

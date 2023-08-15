#!/usr/bin/env python3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
""" Script to create a SQLAlchemy model named User for a
    database table named users """

Base = declarative_base()


class User(Base):
    """ Represent the user table
      - Inherits from the Sql Alchemy Base Class
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)

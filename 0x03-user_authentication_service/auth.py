#!/usr/bin/env python3
"""define a _hash_password method that takes in a password string
    arguments and returns bytes
"""
import bcrypt
import uuid
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """ hashes a pwd"""
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user in the DB"""
        if not email or type(email) != str:
            raise InvalidRequestError("Invalid email format")
        if not password or type(password) != str:
            raise InvalidRequestError("Invalid password format")
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """check if a login is valid"""
        if not email or type(email) != str:
            raise InvalidRequestError("Invalid email format")
        if not password or type(password) != str:
            raise InvalidRequestError("Invalid password format")
        try:
            user = self._db.find_user_by(email=email)
            hashed_pwd = user.hashed_password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pwd):
                return True
        except NoResultFound:
            pass
        return False

    def _generate_uuid(self) -> str:
        """Generate a new UUID string."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """ Create login session"""
        if not email or type(email) != str:
            raise InvalidRequestError("Invalid email format")
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            user_id = user.id
            self._db.update_user(user_id, session_id=session_id)
            return session_id
        except NoResultFound as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ get user using the session id """
        if not session_id or type(session_id) != str:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound as e:
            raise e

    def destroy_session(self, user_id: int) -> None:
        """ Destroy a session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError as e:
            raise e

    def get_reset_password_token(self, email: str) -> str:
        if not email or type(email) != str:
            return None
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = self._generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except ValueError as e:
            raise e


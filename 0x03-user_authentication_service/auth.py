#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
            Args:
                - email: user's email
                - password: user's password
            Return: User instance created
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user's login
            Args:
                - email: user's email
                - password: user's password
            Return: True if the password is correct, False otherwise
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a new session
            Args:
                - email: user's email
            Return: New session ID
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        db.update_user(user.id, session_id=session_id)
        return session_id


def _generate_uuid() -> str:
    """ Generates string representation of a new UUID
    """
    return str(uuid4())

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

    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets user based on their session id
            Args:
                - session_id: user's session_id
            Return: User if found else None
        """
        if not session_id:
            return None
        db = self._db
        try:
            user = db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session
            Args:
                - user_id: user's id
        """
        db = self._db
        db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token
            Args:
                - email: user's email
            Return: Reset token
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates user's password
            Args:
                - reset_token: user's reset token
                - password: user's new password
        """
        db = self._db
        try:
            user = db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        db.update_user(user.id, hashed_password=_hash_password(password))
        db.update_user(user.id, reset_token=None)
        return None


def _generate_uuid() -> str:
    """ Generates string representation of a new UUID
    """
    return str(uuid4())

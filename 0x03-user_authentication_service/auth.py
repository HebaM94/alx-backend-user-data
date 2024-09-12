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

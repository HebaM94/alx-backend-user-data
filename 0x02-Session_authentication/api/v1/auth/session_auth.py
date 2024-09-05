#!/usr/bin/env python3
""" Module of session authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Dict, TypeVar
from uuid import uuid4
from os import getenv


class SessionAuth(Auth):
    """ validate if everything inherits correctly without any overloading
    and the “switch” by using environment variables
    """

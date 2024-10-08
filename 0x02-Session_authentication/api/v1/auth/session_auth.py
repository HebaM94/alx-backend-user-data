#!/usr/bin/env python3
""" Module of session authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4
from os import getenv


class SessionAuth(Auth):
    """ validate if everything inherits correctly without any overloading
    and the “switch” by using environment variables
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get a User ID from a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Get a User instance for a Session ID
        """
        if not request:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        current_user = User.get(user_id)
        return current_user

    def destroy_session(self, request=None) -> bool:
        """ Delete the user session / log out
        """
        if not request:
            return False
        session_id = request.cookies.get(getenv('SESSION_NAME'))
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        SessionAuth.user_id_by_session_id.pop(session_id)
        return True

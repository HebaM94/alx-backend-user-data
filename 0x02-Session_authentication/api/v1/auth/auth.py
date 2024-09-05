#!/usr/bin/env python3
""" Module of API authentication management
"""
from flask import request
from typing import List, TypeVar, Optional
from os import getenv


class Auth:
    """ Class to handle authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required to access path
        """
        if not excluded_paths or not path:
            return True
        path = path if path.endswith('/') else path + '/'
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.strip("*")):
                return False
        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """ Get the authorization header from the request
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user from the request
        """
        return None

    def session_cookie(self, request=None):
        """ Get the session cookie from the request
        """
        if request is None:
            return None
        session_cookie = request.cookies.get(getenv('SESSION_NAME'))
        return session_cookie

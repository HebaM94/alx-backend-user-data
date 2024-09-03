#!/usr/bin/env python3
""" Module of API authentication management
"""
from flask import request
from typing import List, TypeVar, Optional


class Auth:
    """ Class to handle authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required to access path
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
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

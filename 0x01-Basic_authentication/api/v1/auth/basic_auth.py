#!/usr/bin/env python3
"""
Basic authentication module
"""
import binascii
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Optional, Tuple, TypeVar


class BasicAuth(Auth):
    """ Basic authentication class
    """
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """ Retrieves authentication parameters form authorization header
        """
        if not authorization_header or not isinstance(authorization_header,
                                                      str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ Decodes base64 authorization header
        """
        if not base64_authorization_header or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Extracts user credentials from decoded base64 authorization header
        """
        if not decoded_base64_authorization_header or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """ Creates user object from user credentials
        """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        try:
            users = User.search(attributes={"email": user_email})
        except KeyError:
            return None
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

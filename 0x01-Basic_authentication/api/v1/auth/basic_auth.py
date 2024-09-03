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

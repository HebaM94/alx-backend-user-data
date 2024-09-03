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
                                            str) -> Optional[str]:
        """ Retrieves authentication parameters form authorization header
        """
        if not authorization_header or not isinstance(authorization_header,
                                                      str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

#!/usr/bin/python3

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

__all__ = [
    "AuthBearer"
]

from app.core import TOKEN_TEST


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(AuthBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme.")
            self.validate_token(credentials.credentials)
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")

    @staticmethod
    def validate_token(token: str):
        """
        Determines if the Access Token is valid

        :param token:
        """
        if token != TOKEN_TEST:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                detail="invalid token")
        return True

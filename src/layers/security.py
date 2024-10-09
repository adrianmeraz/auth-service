import typing
from enum import Enum

import jwt

from . import logs

logger = logs.get_logger()


class UserRoles(str, Enum):
    MEMBER = 'MEMBER'
    STAFF = 'STAFF'
    SUPERUSER = 'SUPERUSER'


class AuthToken:
    def __init__(self, token):
        # No need to validate token since apigw authorizer already does so
        self.decoded_token = jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})

    @property
    def username(self) -> str:
        return self.decoded_token['cognito:username']

    @property
    def roles(self) -> typing.List[UserRoles]:
        return [UserRoles(r) for r in self.decoded_token['custom:roles'].split(',')]

    @property
    def group(self) -> str:
        return self.decoded_token['custom:group']

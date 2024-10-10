import typing
from enum import Enum

import jwt

from . import logs

logger = logs.get_logger()


class UserRoles(str, Enum):
    MEMBER = 'MEMBER'
    STAFF = 'STAFF'
    SUPERUSER = 'SUPERUSER'


COGNITO_USERNAME_KEY = 'cognito:username'
ROLES_KEY = 'custom:roles'
GROUP_KEY = 'custom:group'


class AuthToken:
    def __init__(self, token):
        # No need to validate token since apigw authorizer already does so
        self.decoded_token = jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})

    @property
    def username(self) -> str:
        return self.decoded_token[COGNITO_USERNAME_KEY]

    @property
    def roles(self) -> typing.List[UserRoles]:
        return [UserRoles(r) for r in self.decoded_token[ROLES_KEY].split(',')]

    @property
    def group(self) -> str:
        return self.decoded_token[GROUP_KEY]

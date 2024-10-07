import typing
from enum import Enum

import jwt

from . import exceptions, logs

logger = logs.get_logger()


class Permissions(str, Enum):
    ADD_MEMBER_USER = 'ADD_MEMBER_USER'
    ADD_ORGANIZATION = 'ADD_ORGANIZATION'
    ADD_STAFF_USER = 'ADD_STAFF_USER'
    ADD_SUPERUSER_USER = 'ADD_SUPERUSER_USER'

    DELETE_MEMBER_USER = 'DELETE_MEMBER_USER'
    DELETE_ORGANIZATION = 'DELETE_ORGANIZATION'
    DELETE_STAFF_USER = 'DELETE_STAFF_USER'
    DELETE_SUPERUSER_USER = 'DELETE_SUPERUSER_USER'

    UPDATE_MEMBER_USER = 'UPDATE_MEMBER_USER'
    UPDATE_ORGANIZATION = 'UPDATE_ORGANIZATION'
    UPDATE_STAFF_USER = 'UPDATE_STAFF_USER'
    UPDATE_SUPERUSER_USER = 'UPDATE_SUPERUSER_USER'

    VIEW_ORGANIZATION = 'VIEW_ORGANIZATION'
    VIEW_USER = 'VIEW_USER'


class UserRoles(str, Enum):
    MEMBER = 'MEMBER'
    STAFF = 'STAFF'
    SUPERUSER = 'SUPERUSER'


__p = Permissions
USER_ROLE_PERMISSIONS_MAP = {
    UserRoles.MEMBER.value: {
        __p.VIEW_ORGANIZATION,
        __p.VIEW_USER
    },
    UserRoles.STAFF.value: {
        __p.ADD_MEMBER_USER,
        __p.DELETE_MEMBER_USER,
        __p.UPDATE_MEMBER_USER,
        __p.VIEW_ORGANIZATION,
        __p.VIEW_USER
    }
}


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
    def org(self) -> str:
        return self.decoded_token['custom:group']

    def validate_org_claim(self, required_org_name: str):
        if required_org_name != self.org:
            logger.warning(
                f'User is not a member of the organization "{required_org_name}"',
                org=self.org,
                username=self.username
            )
            raise exceptions.UserUnauthorizedException()

    def validate_roles_claim(self, required_roles: typing.List[UserRoles]):
        if not set(required_roles).issubset(set(self.roles)):
            logger.warning(
                f'User "{self.username}" with roles "{self.roles}" does not have required roles',
                required_roles=required_roles
            )
            raise exceptions.UserUnauthorizedException()

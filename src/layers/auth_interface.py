from abc import ABC, abstractmethod

from . import security
from .entities import CognitoTokenResponse


class AuthInterface(ABC):
    @classmethod
    @abstractmethod
    def create_admin_user(
        cls,
        email: str,
        group_name: str,
        set_roles: set[security.UserRoles],
        username: str,
    ):
        pass

    @classmethod
    @abstractmethod
    def login(
        cls,
        username: str,
        password: str,
    ) -> CognitoTokenResponse:
        pass

    @classmethod
    @abstractmethod
    def refresh_token(
        cls,
        refresh_token: str
    ) -> CognitoTokenResponse:
        pass

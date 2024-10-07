from abc import ABC, abstractmethod

from . import security
from .entities import CognitoTokenResponse


class AuthInterface(ABC):
    @classmethod
    @abstractmethod
    def create_admin_user(
        cls,
        org_name: str,
        username: str,
        email: str,
        set_roles: set[security.UserRoles],
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

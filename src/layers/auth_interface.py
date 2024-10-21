from abc import ABC, abstractmethod

from . import security
from .entities import CognitoTokenResponse


class IAuth(ABC):
    @abstractmethod
    def create_admin_user(
        self,
        email: str,
        group_name: str,
        set_roles: set[security.UserRoles],
        username: str,
    ):
        pass

    @abstractmethod
    def login(
        self,
        username: str,
        password: str,
    ) -> CognitoTokenResponse:
        pass

    @abstractmethod
    def refresh_token(
        self,
        refresh_token: str
    ) -> CognitoTokenResponse:
        pass

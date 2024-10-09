from .auth_interface import AuthInterface
from .auth_service import AuthService


class ServiceConfig:
    __auth_service = AuthService()

    @classmethod
    def get_auth_service(cls) -> AuthInterface:
        return cls.__auth_service

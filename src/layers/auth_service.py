from botocore.client import BaseClient

from . import auth_cognito, security
from .auth_interface import IAuth
from .entities import CognitoTokenResponse
from .secrets import Secrets


class AuthService(IAuth):
    def __init__(self, boto_client: BaseClient, secrets: Secrets):
        self._boto_client = boto_client
        self._secrets = secrets

    def create_admin_user(
        self,
        group_name: str,
        username: str,
        email: str,
        set_roles: set[security.UserRoles],
    ):
        return auth_cognito.CreateCognitoAdminUser.call(
            boto_client=self._boto_client,
            cognito_pool_id=self._secrets.cognito_pool_id,
            group_name=group_name,
            username=username,
            email=email,
            set_roles=set_roles
        )

    def login(
        self,
        username: str,
        password: str
    ) -> CognitoTokenResponse:
        return auth_cognito.Login.call(
            boto_client=self._boto_client,
            cognito_pool_client_id=self._secrets.cognito_pool_client_id,
            username=username,
            password=password
        ).token_response

    def refresh_token(self, refresh_token: str) -> CognitoTokenResponse:
        return auth_cognito.RefreshToken.call(
            boto_client=self._boto_client,
            cognito_pool_client_id=self._secrets.cognito_pool_client_id,
            refresh_token=refresh_token,
        ).token_response

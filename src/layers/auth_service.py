from py_aws_core import cognito

from . import auth_cognito, security
from .auth_interface import AuthInterface
from .entities import CognitoTokenResponse

cog_client = cognito.CognitoClient()


class AuthService(AuthInterface):
    @classmethod
    def create_admin_user(
        cls,
        org_name: str,
        username: str,
        email: str,
        set_roles: set[security.UserRoles],
    ):
        return auth_cognito.CreateCognitoAdminUser.call(
            cog_client=cog_client,
            org_name=org_name,
            username=username,
            email=email,
            set_roles=set_roles
        )

    @classmethod
    def login(cls, username: str, password: str) -> CognitoTokenResponse:
        return auth_cognito.Login.call(
            cog_client=cog_client,
            username=username,
            password=password
        ).token_response

    @classmethod
    def refresh_token(cls, refresh_token: str) -> CognitoTokenResponse:
        return auth_cognito.RefreshToken.call(
            cog_client=cog_client,
            refresh_token=refresh_token,
        ).token_response

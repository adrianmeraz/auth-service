from botocore.client import BaseClient
from py_aws_core import cognito_api

from . import logs, security
from .auth_interface import IAuth
from .entities import CognitoTokenResponse
from .secrets import Secrets

logger = logs.get_logger()


class AuthService(IAuth):
    def __init__(self, boto_client: BaseClient, secrets: Secrets):
        self._boto_client = boto_client
        self._secrets = secrets
        self._cognito_pool_id = secrets.cognito_pool_id
        self._cognito_pool_client_id = secrets.cognito_pool_client_id

    def create_admin_user(
        self,
        group_name: str,
        username: str,
        email: str,
        set_roles: set[security.UserRoles],
    ):
        return cognito_api.AdminCreateUser.call(
            boto_client=self._boto_client,
            cognito_pool_id=self._cognito_pool_id,
            username=username,
            user_attributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'custom:group',
                    'Value': group_name
                },
                {
                    'Name': 'custom:roles',
                    'Value': ','.join(sorted([r.value for r in set_roles]))
                },
            ],
            desired_delivery_mediums=[
                'EMAIL',
            ],
        )

    def login(
        self,
        username: str,
        password: str
    ) -> CognitoTokenResponse:
        auth_result = cognito_api.UserPasswordAuth.call(
            boto_client=self._boto_client,
            cognito_pool_client_id=self._cognito_pool_client_id,
            username=username,
            password=password
        ).AuthenticationResult
        return CognitoTokenResponse(
            access_token=auth_result.AccessToken,
            refresh_token=auth_result.RefreshToken,
            id_token=auth_result.IdToken
        )

    def refresh_token(self, refresh_token: str) -> CognitoTokenResponse:
        auth_result = cognito_api.RefreshTokenAuth.call(
            boto_client=self._boto_client,
            cognito_pool_client_id=self._cognito_pool_client_id,
            refresh_token=refresh_token,
        ).AuthenticationResult
        return CognitoTokenResponse(
            access_token=auth_result.AccessToken,
            refresh_token=auth_result.RefreshToken,
            id_token=auth_result.IdToken
        )

    def set_user_password(self, username: str, new_password: str) -> CognitoTokenResponse:
        auth_result = cognito_api.RespondToAuthChallenge.call(
            boto_client=self._boto_client,
            cognito_pool_client_id=self._cognito_pool_client_id,
            challenge_name=cognito_api.AuthChallenge.NEW_PASSWORD_REQUIRED,
            challenge_responses=cognito_api.NewPasswordChallengeResponse(
                username=username,
                new_password=new_password
            )
        ).AuthenticationResult
        return CognitoTokenResponse(
            access_token=auth_result.AccessToken,
            refresh_token=auth_result.RefreshToken,
            id_token=auth_result.IdToken
        )

from botocore.client import BaseClient
from py_aws_core import cognito_api

from . import api_responses, logs, security
from .auth_interface import IAuth
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
    ) -> api_responses.CognitoTokenResponse:
        response = cognito_api.UserPasswordAuth.call(
            boto_client=self._boto_client,
            cognito_pool_client_id=self._cognito_pool_client_id,
            username=username,
            password=password
        )
        r_auth = response.AuthenticationResult
        return api_responses.LoginResponse(
            access_token=r_auth.AccessToken,
            refresh_token=r_auth.RefreshToken,
            id_token=r_auth.IdToken,
            session=response.Session,
            challenge_name=response.ChallengeName,
            challenge_parameters=response.ChallengeParameters
        )

    def refresh_token(self, refresh_token: str) -> api_responses.CognitoTokenResponse:
        response = cognito_api.RefreshTokenAuth.call(
            boto_client=self._boto_client,
            cognito_pool_client_id=self._cognito_pool_client_id,
            refresh_token=refresh_token,
        )
        r_auth = response.AuthenticationResult
        return api_responses.CognitoTokenResponse(
            access_token=r_auth.AccessToken,
            refresh_token=r_auth.RefreshToken,
            id_token=r_auth.IdToken,
            session=response.Session
        )

    def set_user_password(self, username: str, new_password: str, session: str = None) -> api_responses.CognitoTokenResponse:
        response = cognito_api.RespondToAuthChallenge.call(
            boto_client=self._boto_client,
            cognito_pool_client_id=self._cognito_pool_client_id,
            challenge_name=cognito_api.AuthChallenge.NEW_PASSWORD_REQUIRED,
            challenge_responses=cognito_api.NewPasswordChallengeResponse(
                username=username,
                new_password=new_password
            ),
            session=session
        )
        r_auth = response.AuthenticationResult
        return api_responses.CognitoTokenResponse(
            access_token=r_auth.AccessToken,
            refresh_token=r_auth.RefreshToken,
            id_token=r_auth.IdToken,
            session=response.Session
        )

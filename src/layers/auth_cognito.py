from dataclasses import dataclass

from botocore.client import BaseClient
from py_aws_core import cognito_api, decorators as aws_decorators, exceptions as aws_exceptions

from . import exceptions, entities, logs, security

logger = logs.get_logger()


class CreateCognitoAdminUser:
    @classmethod
    @aws_decorators.boto3_handler(client_error_map=dict(), raise_as=exceptions.AuthServiceException)
    def call(
        cls,
        boto_client: BaseClient,
        cognito_pool_id: str,
        group_name: str,
        username: str,
        email: str,
        set_roles: set[security.UserRoles],
    ):
        response = cognito_api.AdminCreateUser.call(
            boto_client=boto_client,
            cognito_pool_id=cognito_pool_id,
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
        logger.info('Admin User Created', response=response)
        return response


@dataclass
class CognitoResponse:
    cog_response: cognito_api.RefreshTokenAuth.Response

    @property
    def token_response(self):
        auth_result = self.cog_response.AuthenticationResult
        return entities.CognitoTokenResponse(
            access_token=auth_result.AccessToken,
            id_token=auth_result.IdToken,
            refresh_token=auth_result.RefreshToken
        )


class Login:
    class Response(CognitoResponse):
        pass

    @classmethod
    @aws_decorators.boto3_handler(client_error_map=dict(), raise_as=exceptions.AuthServiceException)
    def call(
        cls,
        boto_client: BaseClient,
        cognito_pool_client_id: str,
        username: str,
        password: str,
    ) -> Response:
        response = cognito_api.UserPasswordAuth.call(
            boto_client=boto_client,
            cognito_pool_client_id=cognito_pool_client_id,
            username=username,
            password=password
        )
        logger.info(f'User "{username}" successfully logged in')
        return cls.Response(cog_response=response)


class RefreshToken:
    class Response(CognitoResponse):
        pass

    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=aws_exceptions.ERR_CODE_MAP, cancellation_err_maps=[])
    def call(
        cls,
        boto_client: BaseClient,
        cognito_pool_client_id: str,
        refresh_token: str,
    ) -> Response:
        response = cognito_api.RefreshTokenAuth.call(
            boto_client=boto_client,
            cognito_pool_client_id=cognito_pool_client_id,
            refresh_token=refresh_token
        )
        logger.info(f'Successfully refreshed token')
        return cls.Response(cog_response=response)

from dataclasses import dataclass

from py_aws_core import cognito, decorators as aws_decorators
from py_aws_core.cognito import CognitoClient

from . import exceptions, entities, logs, security

logger = logs.get_logger()


class CreateCognitoAdminUser:
    @classmethod
    @aws_decorators.boto3_handler(client_error_map=dict(), raise_as=exceptions.AuthServiceException)
    def call(
        cls,
        cog_client: CognitoClient,
        org_name: str,
        username: str,
        email: str,
        set_roles: set[security.UserRoles],
    ):
        return cognito.AdminCreateUser.call(
            client=cog_client,
            username=username,
            user_attributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'custom:group',
                    'Value': org_name
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


@dataclass
class CognitoResponse:
    cog_response: cognito.RefreshTokenAuth.Response

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

    # TODO Pool and client id should be passed as params, and not part of client
    @classmethod
    @aws_decorators.boto3_handler(client_error_map=dict(), raise_as=exceptions.AuthServiceException)
    def call(
            cls,
            cog_client: CognitoClient,
            username: str,
            password: str,
            pool_client_id: str,
            pool_id: str,
    ) -> Response:
        response = cognito.UserPasswordAuth.call(
            client=cog_client,
            username=username,
            password=password
        )
        logger.info(f'User "{username}" successfully logged in')
        return cls.Response(cog_response=response.AuthenticationResult)


class RefreshToken:
    class Response(CognitoResponse):
        pass

    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=exceptions.ERR_CODE_MAP, cancellation_err_maps=[])
    def call(
        cls,
        cog_client: CognitoClient,
        refresh_token: str,
    ) -> Response:
        response = cognito.RefreshTokenAuth.call(
            client=cog_client,
            refresh_token=refresh_token
        )
        logger.info(f'Successfully refreshed token')
        return cls.Response(cog_response=response.AuthenticationResult)

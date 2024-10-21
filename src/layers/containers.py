from dependency_injector import containers, providers
from py_aws_core.boto_clients import CognitoClientFactory, DynamoDBClientFactory, SSMClientFactory
from py_aws_core.router import APIGatewayRouter

from .auth_service import AuthService
from .secrets import Secrets


class Container(containers.DeclarativeContainer):

    api_gw_router = APIGatewayRouter()

    cognito_client = providers.Factory(CognitoClientFactory.new_client)
    dynamo_db_client = providers.Factory(DynamoDBClientFactory.new_client)
    ssm_client = providers.Factory(SSMClientFactory.new_client)

    secrets = providers.Singleton(Secrets, boto_client=ssm_client)

    auth_service = providers.Factory(AuthService, boto_client=cognito_client, secrets=secrets)

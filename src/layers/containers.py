from dependency_injector import containers, providers
from py_aws_core.boto_clients import CognitoClient, DynamoTable, SSMClient
from py_aws_core.router import APIGatewayRouter

from .auth_service import AuthService
from .secrets import Secrets


class Container(containers.DeclarativeContainer):

    api_gw_router = APIGatewayRouter()

    ssm_client = providers.Factory(SSMClient)
    secrets = providers.Singleton(Secrets, ssm_client=ssm_client)

    cognito_client = providers.Factory(CognitoClient)
    dynamo_table = providers.Factory(DynamoTable, ddb_secrets=secrets)

    auth_service = providers.Factory(AuthService, boto_client=cognito_client, secrets=secrets)

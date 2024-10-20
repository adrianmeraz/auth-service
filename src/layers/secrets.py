from botocore.client import BaseClient
from py_aws_core.ssm_parameter_store import SSMParameterStore


class Secrets(SSMParameterStore):
    APP_NAME_KEY = 'APP_NAME'
    AWS_COGNITO_POOL_ID_KEY = 'AWS_COGNITO_POOL_ID'
    AWS_COGNITO_POOL_CLIENT_ID_KEY = 'AWS_COGNITO_POOL_CLIENT_ID'
    AWS_DYNAMO_DB_TABLE_NAME_KEY = 'AWS_DYNAMO_DB_TABLE_NAME'
    ENVIRONMENT_KEY = 'ENVIRONMENT'

    def __init__(
        self,
        boto_client: BaseClient,
        app_name: str = None,
        aws_cognito_pool_id: str = None,
        aws_cognito_pool_client_id: str = None,
        aws_dynamo_db_table_name: str = None,
        environment: str = None,
    ):
        super().__init__(
            boto_client=boto_client,
            cached_secrets={
                self.APP_NAME_KEY: app_name,
                self.AWS_COGNITO_POOL_ID_KEY: aws_cognito_pool_id,
                self.AWS_COGNITO_POOL_CLIENT_ID_KEY: aws_cognito_pool_client_id,
                self.AWS_DYNAMO_DB_TABLE_NAME_KEY: aws_dynamo_db_table_name,
                self.ENVIRONMENT_KEY: environment,
            }
        )

    @property
    def app_name(self) -> str:
        return self.get_secret(self.APP_NAME_KEY)

    @property
    def cognito_pool_id(self) -> str:
        return self.get_secret(self.AWS_COGNITO_POOL_ID_KEY)

    @property
    def cognito_pool_client_id(self) -> str:
        return self.get_secret(self.AWS_COGNITO_POOL_CLIENT_ID_KEY)

    @property
    def dynamo_db_table_name(self) -> str:
        return self.get_secret(self.AWS_DYNAMO_DB_TABLE_NAME_KEY)

    @property
    def environment(self) -> str:
        return self.get_secret(self.ENVIRONMENT_KEY)

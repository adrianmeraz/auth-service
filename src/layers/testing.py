from importlib.resources import files

from py_aws_core.boto_clients import SSMClientFactory
from py_aws_core.testing import BaseTestFixture

from src.layers.secrets import Secrets


class ASTestFixture(BaseTestFixture):
    TEST_RESOURCE_PATH = files('tests._resources')

    TEST_API_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('api')
    TEST_COGNITO_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('cognito')
    TEST_DB_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('db')
    TEST_EVENT_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('events')

    TEST_COGNITO_POOL_CLIENT_ID = '7xxxxtgbdebch6fffffueq2h1m'
    TEST_COGNITO_POOL_ID = 'us-west-2_CCCQW5ZZZ'

    @classmethod
    def get_api_resource_json(cls, *descendants) -> dict:
        return cls.get_resource_json(*descendants, path=cls.TEST_API_RESOURCE_PATH)

    @classmethod
    def get_cognito_resource_json(cls, *descendants) -> dict:
        return cls.get_resource_json(*descendants, path=cls.TEST_COGNITO_RESOURCE_PATH)

    @classmethod
    def get_db_resource_json(cls, *descendants) -> dict:
        return cls.get_resource_json(*descendants, path=cls.TEST_DB_RESOURCE_PATH)

    @classmethod
    def get_event_resource_json(cls,  *descendants) -> dict:
        return cls.get_resource_json(*descendants, path=cls.TEST_EVENT_RESOURCE_PATH)

    @classmethod
    def get_mocked_secrets(cls):
        boto_client = SSMClientFactory.new_client()
        return Secrets(
            app_name='big-service',
            boto_client=boto_client,
            base_domain_name='ipsumlorem.com',
            cognito_pool_id=cls.TEST_COGNITO_POOL_ID,
            cognito_pool_client_id=cls.TEST_COGNITO_POOL_CLIENT_ID,
            dynamo_db_table_name='TEST_TABLE',
            environment='dev',
        )


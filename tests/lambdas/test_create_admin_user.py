from botocore.stub import Stubber
from py_aws_core.boto_clients import CognitoClient

from src.lambdas import create_admin_user
from src.layers.auth_service import AuthService
from src.layers.testing import ASTestFixture


class CreateAdminUserTests(ASTestFixture):
    def test_ok(self):
        cognito_client = CognitoClient()
        boto_client = cognito_client.boto_client

        stubber_1 = Stubber(boto_client)
        admin_create_user_json = self.get_cognito_resource_json('cognito#admin_create_user.json')
        stubber_1.add_response(method='admin_create_user', service_response=admin_create_user_json)
        stubber_1.activate()

        mock_event = self.get_event_resource_json('event#create_admin_user.json')
        secrets = self.get_mocked_secrets()
        auth_service = AuthService(cognito_client=cognito_client, secrets=secrets)

        val = create_admin_user.lambda_handler(event=mock_event, context=None, auth_service=auth_service)
        self.assertEqual(
            val,
            {
                'body': '{}',
                'multiValueHeaders': {
                    'Access-Control-Allow-Credentials': [True],
                    'Access-Control-Allow-Headers': ['Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'],
                    'Access-Control-Allow-Methods': ['DELETE,GET,POST,PUT'],
                    'Access-Control-Allow-Origin': ['*'],
                    'Content-Type': ['application/json']
                },
                'isBase64Encoded': False,
                'statusCode': 200
            }
        )

        stubber_1.assert_no_pending_responses()

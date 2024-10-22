from botocore.stub import Stubber
from py_aws_core.boto_clients import CognitoClientFactory

from src.lambdas import set_user_password
from src.layers.auth_service import AuthService
from src.layers.testing import ASTestFixture


class SetNewUserPasswordTests(ASTestFixture):
    def test_ok(self):
        boto_client = CognitoClientFactory.new_client()

        stubber_1 = Stubber(boto_client)
        initiate_auth_json = self.get_cognito_resource_json('cognito#initiate_auth.json')
        stubber_1.add_response(method='initiate_auth', service_response=initiate_auth_json)
        stubber_1.activate()

        mock_event = self.get_event_resource_json('event#set_user_password.json')
        secrets = self.get_mocked_secrets()
        auth_service = AuthService(boto_client=boto_client, secrets=secrets)

        val = set_user_password.lambda_handler(event=mock_event, context=None, auth_service=auth_service)
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

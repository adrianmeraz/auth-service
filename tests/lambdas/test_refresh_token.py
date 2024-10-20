from botocore.stub import Stubber
from py_aws_core.boto_clients import CognitoClientFactory

from src.lambdas import refresh_token
from src.layers.auth_service import AuthService
from src.layers.testing import ASTestFixture


class RefreshTokenApiTests(ASTestFixture):
    def test_ok(self):
        boto_client = CognitoClientFactory.new_client()

        stubber_1 = Stubber(boto_client)
        initiate_auth_json = self.get_cognito_resource_json('cognito#initiate_auth.json')
        stubber_1.add_response(method='initiate_auth', service_response=initiate_auth_json)
        stubber_1.activate()

        mock_event = self.get_event_resource_json('event#refresh_token.json')
        secrets = self.get_mocked_secrets()
        auth_service = AuthService(boto_client=boto_client, secrets=secrets)

        val = refresh_token.lambda_handler(event=mock_event, context=None, auth_service=auth_service)
        self.assertEqual(
            val,
            {
                'body': '{"access_token": "eyJraWQiOiJzbVUyd3lwQ2QyQ1lhYVhCbW04OUZHU3pkZXBxZ1wvVFlsZUdQS3ZKQ1NWTT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzZTYyYzNjOC00OTcwLTRmYzctYTk5Ni04NjhkNGMxMzk3ZjYiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9DeFZRVzVNcFUiLCJjbGllbnRfaWQiOiI3bXVkdXRnYmRlYmNoNmFlaDIxdWVxMmgxbSIsIm9yaWdpbl9qdGkiOiIwMjk5ZjdlNi1kYjdiLTQ3M2YtODZiOC05M2FkY2EyMGQ1MGUiLCJldmVudF9pZCI6IjExNjQxNmE0LTAxN2EtNGMyYi1iOTNhLWNmZGRiYWUyYzYyNyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3MTU3ODUzNDgsImV4cCI6MTcxNTc4ODk0OCwiaWF0IjoxNzE1Nzg1MzQ4LCJqdGkiOiI1MTQ2YjgwMS1kZGM4LTQ0MzUtYmQ3NC0zNjU4MjQ0OGRkYjUiLCJ1c2VybmFtZSI6ImhlbGxvbW90byJ9.EWjr8Fcf_a6cg_VVvXNVqjkndd33qN2cLeJg16rqwLvF4qzJAQK3Qjt4QgjTm8pOjyL1qoz2U1HJP2kSqJIuujSJi3aTcyE-1N7O7SWe3yqhAAuJ15FaGA55tyJ7hC6jhkotXGufxo6-SolHqcDMtNGDBtC5XH4b8ea9RJdnbSZhG43AnlbsfSrCz7GOpQiasyhArSieTEeiZysDKgObLK9U35fzV5cjss4UWEaf3jG1NFuUtA8GsamvWMVxKVDIv72kmfU9nlUWry4UrLkT7nX9QlenPL3LC1KiO6ar_iRwUP_tEBjcg62TBeyfhOn0lTUjvV-vySR2ZkEt-oJItQ", "refresh_token": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.iD5hrQ0SrYfnj71rygJlyW540l8JJzevGhEpIz_hW63ehwED9Wu0sjTFJ0rvoIM7TtKayfnuu9jrKo1g0l4zo9NF18yNhLxm7QiQ0JlzQkZppWJSYYXNYNaTampwF9r57AKgpDJupHKbuGWHW9soDYfu07xP4m6O3ibLOEv9sYFGnT8mFLu_2xUZXShl4gnrj9fVmn4ayk7Lz9X_E74TYvEL-kxcV2mbrgFzxUvgfaYwNWnj8N0OpfDC5wU3DV58IBhHHDKMXmvfEm5zLbqsSfQGcjZdrUGX3NBSe1YkaJ0ASz8qXLmwywocg23MWaCcFikUIke7v6t2dO1Eukdp8g.CCiZSgN7fto2NzJG.QObyv2K-XCkJK8Mxbab1peV6jTaUpuzerAInsOh-8FbLwGmpoh0HAkgcn1WVhH7xl2ulmcz3miknh4xb1JL_gnHyIOwr1soso7BnxKYGjqi3Kax6VUgNXd4TdJJtMfMNbWgudEQc8MKR46REyB4qVEjUqAf4Sk11IF_eshOuBBmmiBRxKDSZ7K9aPuAZ7WqTWemysytzfR5Sr9QtENqX-cq2qXJWralrvs0FIglN8B2aBAq2eF_mZetU7rNZRAfp1MSI9-1dvIVvs8zezqKfTaP3dOBGLqUzmhzIeP4rMpkqWdyrXTgDujwA1zGsHOxl4Rd3t2Q7pOBfLT6xk0MByXlLLpyzLiiPBC1NVEibWLx2yS1B8-_jzKpeeUDnCKiNbsMG60QkzIn0ez_RuQVOLSxASHoWAfeSgqDYWJqkMb5EsrLim03j0ZQthexbjv3K9n7Ni6T1_OPVZPT3WsaLYy__d2o7bodAeF-K9NSfvqOMyt6cF3ILxMLqP21Y8GJCEWLqBxIE2IdKl6YSySBG8LECWaupUEtZxFxfcx0UjPI84YZ05Deth34EEI6r94Kmi-PV5P5aOZOsdbQSweXzyOyDEFGkCuLCWC-hslQtwcm5rmvc9bGPA6YtyPLaP9wzUCjjOWdX6NoWQ1a__Ed_fyoKB0Fuk1-92PI39SrFYkRS6HCfIIZmICkKrqAN27m2fJWguYN0B43GLnHC7nRhvqpsOu0ilYKq70nrCwie8I0bPOicgUSjFxI3dfzO0fLqUuD4M3D0P3bcjI5lyYeK9bwD8rTXF0USv6le0GlJr6tnUy_H1JggWoyy4_bMTK1AML-vyPCtR1d2mxpNLbhkEBSWJS6Npm34DPfQbLF3tVBfs_OLah0pIslW9JPcBFl6vR5bu5xCohgqcyIRV_7tOMUoXJSRc2BJoxhbgNo_pDLz-BxbDFS4kGT6Ebdx39RKGC7M8bG0s8deojPAkyMFapRpMLTCRC8WC0Lkz81vm3ho9tnRqYx-e5lLxV61buxTzFSJ-Dqy5ev6Pm9aNfSfFfiJd1wn9-hAfh5dhaWxdJ0sOnyQAMSp4GiiFL8V5_P4t4TPK1K8s3mz0vH28a7IKON0CLrEKJ6nPyXpsIEM_lrweN2p1r51ognP7MA7SKTHeQkBNc9BIrRxwNkf9gpKM9nVhH8Y4dU3HjRG4Tcx7IwkFBwBJ4U122_dHbml7Nyl4l5s6S58VSXokVajE5xGo4_WsWrVU0XZaPs2wpm-rwQ6vNuc_G7S4_7i6zhaVbDDUrIZ9NroBF4.bLQ7aQ2rbs2-ToRJU-aa8Q", "id_token": "eyJraWQiOiJzNndrcytDXC84WGxNOVF2OHNYeVhGczNjV1VsOVFwVzZsdE9rMGt5R2dDVT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzZTYyYzNjOC00OTcwLTRmYzctYTk5Ni04NjhkNGMxMzk3ZjYiLCJjdXN0b206cm9sZXMiOiJTVVBFUlVTRVIsTUVNQkVSLFNUQUZGIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yX0N4VlFXNU1wVSIsImN1c3RvbTpncm91cCI6Indob2FkZXJlanIiLCJjb2duaXRvOnVzZXJuYW1lIjoiaGVsbG9tb3RvIiwib3JpZ2luX2p0aSI6IjAyOTlmN2U2LWRiN2ItNDczZi04NmI4LTkzYWRjYTIwZDUwZSIsImF1ZCI6IjdtdWR1dGdiZGViY2g2YWVoMjF1ZXEyaDFtIiwiZXZlbnRfaWQiOiIxMTY0MTZhNC0wMTdhLTRjMmItYjkzYS1jZmRkYmFlMmM2MjciLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTcxNTc4NTM0OCwiZXhwIjoxNzE1Nzg4OTQ4LCJpYXQiOjE3MTU3ODUzNDgsImp0aSI6IjhiMTJmMGQ2LTIyN2UtNDg2Mi1hMGY2LTIxMzEwNjFlMjg4NSIsImVtYWlsIjoiYWRyaWFuQHJ5ZGVhcy5jb20ifQ.fnMRLUYuzVe2cFPnDSrZXhT34bV8SY6SpXqmCtMbwXcFep13JleLdgQ52HNlR8d0OSF26yw612jCXg8DIHV6IxP7miazovAESF1nBrBpYXV70oXeXmi_6UJ6cYxr9XT4cG6iigsJufrc6LvEl_9iOGnvstotrSD_N0hsfpZG0QTeMY8odZIz71_eGFsJqtsIQFZMrAOqRfOxGf1Xnj0AhM9zf5amGAyWpmxKnRVDl2RFi-ZFhellzFZMcQMjawz-CBFQz5lXac-pukiWJgjTjx4macQl7d-7_kDnQWf_aIgsW27SEQKtc9Z885zubAkEXokbbpk1QUEKUtl5TR2EPQ"}',
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
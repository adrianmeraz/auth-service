from dependency_injector.wiring import Provide, inject
from py_aws_core import utils as aws_utils

from src.layers import logs
from src.layers.auth_interface import IAuth
from src.layers.containers import Container
from src.layers.events import RefreshTokenEvent

logger = logs.get_logger()

apigw_router = Container.api_gw_router


@apigw_router.route(path='/refresh-token', http_method='POST')
@inject
def lambda_handler(event, context, auth_service: IAuth = Provide[Container.auth_service]):
    event = RefreshTokenEvent(event)
    response = process_event(event=event, auth_service=auth_service)
    return aws_utils.build_lambda_response(
        status_code=200,
        body=response.as_dict()
    )


def process_event(event: RefreshTokenEvent, auth_service: IAuth):
    return refresh_token(event=event, auth_service=auth_service)


def refresh_token(event: RefreshTokenEvent, auth_service: IAuth):
    fields = event.fields
    return auth_service.refresh_token(
        refresh_token=fields.refresh_token
    )

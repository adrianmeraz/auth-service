from dependency_injector.wiring import Provide, inject
from py_aws_core import utils as aws_utils

from src.layers import logs
from src.layers.auth_interface import IAuth
from src.layers.containers import Container
from src.layers.events import LoginEvent

logger = logs.get_logger()

apigw_router = Container.api_gw_router


@apigw_router.route(path='/login', http_method='POST')
@inject
def lambda_handler(event, context, auth_service: IAuth = Provide[Container.auth_service]):
    event = LoginEvent(event)
    process_event(event=event, auth_service=auth_service)
    return aws_utils.build_lambda_response(
        status_code=200,
        body={}
    )


def process_event(event: LoginEvent, auth_service: IAuth):
    return login(event=event, auth_service=auth_service)


def login(event: LoginEvent, auth_service: IAuth):
    fields = event.fields
    return auth_service.login(
        username=fields.username,
        password=fields.password,
    )

from py_aws_core import utils as aws_utils

from src.layers import logs
from src.layers.events import AddUserEvent
from src.layers.routing import get_router
from src.layers.services import ServiceConfig

logger = logs.get_logger()
apigw_router = get_router()
auth_service = ServiceConfig.get_auth_service()


@apigw_router.route(path='/admin-user', http_method='POST')
def lambda_handler(event, context):
    event = AddUserEvent(event)
    process_event(event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body={}
    )


def process_event(event: AddUserEvent):
    return add_member_user(event)


def add_member_user(event: AddUserEvent):
    user = event.user
    return db_service.create_member_user(
        auth_service=auth_service,
        called_by=event.called_by,
        org_name=user.org_name,
        username=user.username,
        first_name=user.first_name,
        first_last_name=user.first_last_name,
        email=user.email,
    )

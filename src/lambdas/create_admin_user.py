from py_aws_core import utils as aws_utils

from src.layers import logs
from src.layers.events import CreateAdminUserEvent
from src.layers.routing import get_router
from src.layers.services import ServiceConfig

logger = logs.get_logger()
apigw_router = get_router()
auth_service = ServiceConfig.get_auth_service()


@apigw_router.route(path='/admin-user', http_method='POST')
def lambda_handler(event, context):
    event = CreateAdminUserEvent(event)
    process_event(event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body={}
    )


def process_event(event: CreateAdminUserEvent):
    return add_member_user(event)


def add_member_user(event: CreateAdminUserEvent):
    fields = event.fields
    return auth_service.create_admin_user(
        email=fields.email,
        group_name=fields.group_name,
        set_roles=fields.set_roles,
        username=fields.username,
    )

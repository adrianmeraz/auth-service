from py_aws_core import decorators

from src.layers import exceptions
from src.layers.containers import Container

apigw_router = Container.api_gw_router


@decorators.lambda_response_handler(raise_as=exceptions.ASCoreException)
def lambda_handler(event, context):
    return apigw_router.handle_event(aws_event=event, aws_context=context)



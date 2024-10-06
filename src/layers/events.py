from py_aws_core.events import LambdaEvent

from . import logs

logger = logs.get_logger()


class HttpEvent(LambdaEvent):
    pass

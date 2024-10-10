import typing

from py_aws_core.events import LambdaEvent
from pydantic import BaseModel, EmailStr

from . import logs, security

logger = logs.get_logger()


class ASEvent(LambdaEvent):
    pass


class CreateAdminUserEvent(ASEvent):
    class CreateAdminUser(BaseModel):
        email = EmailStr
        group_name: str
        set_roles = typing.List[security.UserRoles]
        username: str

    def __init__(self, data):
        super().__init__(data)
        self.fields = self.CreateAdminUser(**self.body)
        # self.group_name = self.body['group_name']
        # self.username = self.body['username']
        # self.email = self.body['email']
        # self.first_name = self.body['set_roles']

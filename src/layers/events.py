from py_aws_core.events import LambdaEvent
from pydantic import BaseModel, EmailStr

from . import logs, security

logger = logs.get_logger()


class ASEvent(LambdaEvent):
    pass


class CreateAdminUserEvent(ASEvent):
    class CreateAdminUser(BaseModel):
        email: EmailStr
        group_name: str
        set_roles: list[security.UserRoles]
        username: str

    def __init__(self, data):
        super().__init__(data)
        self.fields = self.CreateAdminUser(**self.body)


class LoginEvent(ASEvent):
    class Login(BaseModel):
        username: str
        password: str

    def __init__(self, data):
        super().__init__(data)
        self.fields = self.Login(**self.body)


class RefreshTokenEvent(ASEvent):
    class Refresh(BaseModel):
        refresh_token: str

    def __init__(self, data):
        super().__init__(data)
        self.fields = self.Refresh(**self.body)

from dataclasses import dataclass

from py_aws_core.mixins import AsDictMixin


@dataclass
class CognitoTokenResponse(AsDictMixin):
    access_token: str = None
    refresh_token: str = None
    id_token: str = None
    session: str = None


@dataclass(kw_only=True)
class LoginResponse(CognitoTokenResponse):
    challenge_parameters: dict = None
    challenge_name: str = None

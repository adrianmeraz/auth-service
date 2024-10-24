from dataclasses import dataclass

from py_aws_core.mixins import AsDictMixin


@dataclass(kw_only=True)
class CognitoTokenResponse(AsDictMixin):
    access_token: str
    refresh_token: str
    id_token: str
    session: str


@dataclass(kw_only=True)
class LoginResponse(CognitoTokenResponse):
    challenge_parameters: dict
    challenge_name: str

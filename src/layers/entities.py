from dataclasses import dataclass

from py_aws_core.mixins import AsDictMixin


@dataclass
class CognitoTokenResponse(AsDictMixin):
    access_token: str
    refresh_token: str
    id_token: str

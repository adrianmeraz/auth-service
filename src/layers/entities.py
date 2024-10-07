from abc import ABC
from dataclasses import dataclass, asdict

from py_aws_core.mixins import AsDictMixin


@dataclass
class ABCModel(ABC, AsDictMixin):
    _type: str
    created_at: str
    created_by: str

    def as_dict(self):
        return asdict(self)


@dataclass
class Organization(ABCModel):
    billing_plan: str
    status: str
    name: str


@dataclass
class User(ABCModel):
    email: str
    status: str
    first_name: str
    first_last_name: str
    username: str


@dataclass
class UserEmail(ABCModel):
    email: str


@dataclass
class CognitoTokenResponse(AsDictMixin):
    access_token: str
    refresh_token: str
    id_token: str

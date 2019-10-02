from attr import attrs, attrib
from typing import List

from truework import Company
from truework.base import (
    RetrievableAPIResource,
    ListableAPIResource,
    CreatableAPIResource,
)
from truework.price import Price
from truework.turnaround_time import TurnaroundTime


@attrs(frozen=True)
class Target(object):
    company = attrib(type=Company)
    first_name = attrib()
    last_name = attrib()
    social_security_number = attrib()
    contact_email = attrib(default=None)


@attrs(frozen=True)
class Document(object):
    filename = attrib()


@attrs(frozen=True)
class VerificationRequest(
    CreatableAPIResource, RetrievableAPIResource, ListableAPIResource
):
    PATH = "verification-requests/"

    id = attrib()
    created = attrib()
    state = attrib(default=None)
    price = attrib(type=Price, default=None)
    turnaround_time = attrib(type=TurnaroundTime, default=None)
    permissible_purpose = attrib(default=None)
    target = attrib(type=Target, default=None)
    type = attrib(default=None)
    documents = attrib(type=List[Document], default=None)

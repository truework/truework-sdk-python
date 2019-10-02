from attr import attrs, attrib

from truework.base import SearchableAPIResource


@attrs(frozen=True)
class Company(SearchableAPIResource):
    PATH = "companies/"

    name = attrib()
    id = attrib(default=None)
    domain = attrib(default=None)

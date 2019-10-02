from attr import attrs, attrib

from truework.address import Address


@attrs(frozen=True)
class Employer(object):
    name = attrib()
    address = attrib(type=Address, default=None)

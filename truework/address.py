from attr import attrs, attrib


@attrs(frozen=True)
class Address(object):
    line_one = attrib(default=None)
    line_two = attrib(default=None)
    city = attrib(default=None)
    state = attrib(default=None)
    country = attrib(default=None)
    postal_code = attrib(default=None)

from attr import attrs, attrib


@attrs(frozen=True)
class Respondent(object):
    full_name = attrib(default=None)
    address = attrib(default=None)

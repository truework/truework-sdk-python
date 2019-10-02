from attr import attrs, attrib


@attrs(frozen=True)
class TurnaroundTime(object):
    upper_bound = attrib(default=None)
    lower_bound = attrib(default=None)

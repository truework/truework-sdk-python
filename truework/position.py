from attr import attrs, attrib


@attrs(frozen=True)
class Position(object):
    title = attrib()
    start_date = attrib()
    end_date = attrib(default=None)

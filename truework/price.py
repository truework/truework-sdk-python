from attr import attrs, attrib


@attrs(frozen=True)
class Price(object):
    amount = attrib()
    currency = attrib()

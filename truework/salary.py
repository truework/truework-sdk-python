from attr import attrs, attrib


@attrs(frozen=True)
class Salary(object):
    gross_pay = attrib()
    pay_frequency = attrib()
    hours_per_week = attrib()

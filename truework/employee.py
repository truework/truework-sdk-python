from attr import attrs, attrib

from truework.earnings import Earnings
from truework.position import Position
from truework.salary import Salary
from typing import List


@attrs(frozen=True)
class Employee(object):
    first_name = attrib()
    last_name = attrib()
    status = attrib()
    hired_date = attrib()
    end_of_employment = attrib()
    earnings = attrib(type=List[Earnings])
    positions = attrib(type=List[Position])
    salary = attrib(type=Salary)

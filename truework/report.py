from attr import attrs, attrib

from truework import VerificationRequest
from truework.base import RetrievableAPIResource, APIClient
from truework.employee import Employee
from truework.employer import Employer
from truework.respondent import Respondent


@attrs(frozen=True)
class Report(RetrievableAPIResource):
    PATH = "verification-requests/"
    SUB_PATH = "report/"

    @classmethod
    def url_with_id(cls, id):
        from truework import BASE_URL

        return "{}{}{}/{}".format(BASE_URL, cls.PATH, id, cls.SUB_PATH)

    created = attrib()
    current_as_of = attrib()
    verification_request = attrib(type=VerificationRequest)
    employer = attrib(type=Employer)
    employee = attrib(type=Employee)
    additional_notes = attrib(default=None)
    respondent = attrib(type=Respondent, default=None)

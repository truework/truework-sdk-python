import cattr
import requests_mock
from unittest import TestCase

from tests.utils import FixtureLoader
from truework.verification_request import VerificationRequest


class TestVerificationRequestsList(TestCase, FixtureLoader):
    @requests_mock.mock()
    def test_list_success(self, requests_mock):
        requests_mock.get(
            "{}{}".format(VerificationRequest.url(), "?offset=0&limit=5"),
            status_code=200,
            json=self.load_fixture(
                "verification_requests/verification_request_list_response.json"
            ),
        )

        response = VerificationRequest.list(offset=0, limit=5)
        results = list(response.results)

        expected_request = {
            "id": "AAAAAAAAQnIAAYd5YHFVOm8PNX2ecFbEjqV__upOKUE8YE_IK2GwSQTP1",
            "state": "pending-approval",
            "created": "2008-09-15T15:53:00Z",
            "type": "employment-income",
            "price": {"amount": "39.95", "currency": "USD"},
            "turnaround_time": {},
            "permissible_purpose": "credit-application",
            "target": {
                "first_name": "John",
                "last_name": "Doe",
                "contact_email": "johndoe@truework.com",
                "social_security_number": "***-**-0001",
                "company": {"name": "Admazely"},
            },
            "documents": [{"filename": "employee_authorization.pdf"}],
        }

        self.assertEqual(len(results), 5)
        self.assertEqual(
            results[0], cattr.structure(expected_request, VerificationRequest)
        )
        self.assertEqual(
            response.next_url,
            "https://api.truework.com/verification-requests/?offset=5",
        )
        self.assertEqual(response.num_results, 25)

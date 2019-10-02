import cattr
import requests_mock
from unittest import TestCase

from tests.utils import FixtureLoader
from truework.base import TrueworkHTTPError
from truework.verification_request import VerificationRequest


class TestVerificationRequestsRetrieve(TestCase, FixtureLoader):
    @requests_mock.mock()
    def test_retrieve_success(self, mock):
        verification_id = "AAAAAAAAQnIAAYd5YHFVOm8PNX2ecFbEjqV__upOKUE8YE_IK2GwSQTP"
        url = VerificationRequest.url_with_id(verification_id)

        retrieve_response = self.load_fixture(
            "verification_requests/verification_request_retrieve_response.json"
        )

        mock.get(url, status_code=200, json=retrieve_response)

        verification_request = VerificationRequest.retrieve(verification_id)

        self.assertEqual(
            verification_request,
            cattr.structure(retrieve_response, VerificationRequest),
        )

    @requests_mock.mock()
    def test_retrieve_failure(self, mock):
        mock.get(VerificationRequest.url_with_id("1234"), status_code=404)

        with self.assertRaises(TrueworkHTTPError) as context:
            VerificationRequest.retrieve("1234")

        self.assertEqual(context.exception.status_code, 404)

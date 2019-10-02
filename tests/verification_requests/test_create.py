import cattr
import requests_mock
from unittest import TestCase

from tests.utils import FixtureLoader
from truework.base import TrueworkHTTPError
from truework.verification_request import VerificationRequest


class TestVerificationRequestsCreate(TestCase, FixtureLoader):
    @requests_mock.mock()
    def test_create_success(self, mock):
        verification_request_response = self.load_fixture(
            "verification_requests/verification_request_response.json"
        )
        mock.post(
            VerificationRequest.url(),
            status_code=200,
            json=verification_request_response,
        )

        data = {
            "type": "employment",
            "permissible_purpose": "risk-assessment",
            "target": {
                "first_name": "Joe",
                "last_name": "Smith",
                "social_security_number": "000-00-0000",
                "contact_email": "joesmith@example.org",
                "company": {"id": "1234"},
            },
            "documents": [
                {
                    "filename": "signed_auth_form.pdf",
                    "content": "iVBORw0KGgoAAAANSUhEUg......IhAAAAABJRU5ErkJggg==",
                },
                {
                    "filename": "verifier_notes.pdf",
                    "content": "iVBORw0KGgoAAAANSUhEUg......IhAAAAABJRU5FRSJghg==",
                },
            ],
        }

        response = VerificationRequest.create(**data)
        self.assertEqual(
            response,
            cattr.structure(verification_request_response, VerificationRequest),
        )

    @requests_mock.mock()
    def test_create_missing_data(self, mock):
        mock.post(
            VerificationRequest.url(),
            status_code=400,
            json={"error": {"message": "missing type field"}},
        )

        data = {
            "permissible_purpose": "risk-assessment",
            "target": {
                "first_name": "Joe",
                "last_name": "Smith",
                "social_security_number": "000-00-0000",
                "contact_email": "joesmith@example.org",
                "company": {"id": "1234"},
            },
            "documents": [
                {
                    "filename": "signed_auth_form.pdf",
                    "content": "iVBORw0KGgoAAAANSUhEUg......IhAAAAABJRU5ErkJggg==",
                },
                {
                    "filename": "verifier_notes.pdf",
                    "content": "iVBORw0KGgoAAAANSUhEUg......IhAAAAABJRU5FRSJghg==",
                },
            ],
        }

        with self.assertRaises(TrueworkHTTPError) as context:
            VerificationRequest.create(**data)

        self.assertEqual(context.exception.status_code, 400)

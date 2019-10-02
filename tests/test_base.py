import unittest
import requests_mock

import truework
from tests.utils import FixtureLoader
from truework import Company
from truework.base import TrueworkHTTPError


def header_matcher(request):
    return (
        "Authorization" in request.headers
        and request.headers["Authorization"] == "Bearer test_token"
    )


class TestCompanySearch(unittest.TestCase, FixtureLoader):
    @requests_mock.mock()
    def test_invalid_token(self, mock):
        mock.get(
            "{}{}".format(Company.url(), "?offset=0&limit=25&q=International"),
            status_code=401,
            headers={"HTTP_AUTHORIZATION": "Bearer wrong_token"},
            json=self.load_fixture("company/invalid_token.json"),
        )

        with self.assertRaises(TrueworkHTTPError) as context:
            Company.search("International")

        self.assertEqual(context.exception.status_code, 401)

    @requests_mock.mock()
    def test_authentication(self, mock):
        truework.API_TOKEN = "test_token"

        mock.get(
            "{}{}".format(Company.url(), "?offset=0&limit=25&q=International"),
            status_code=200,
            headers={"HTTP_AUTHORIZATION": "Bearer test_token"},
            json=self.load_fixture("company/search_manual_pagination.json"),
            additional_matcher=header_matcher,
        )

        Company.search("International")
        # No need to assert success, as request_mocks would raise an exception if the headers don't match.

    @requests_mock.mock()
    def test_accept_header(self, mock):
        def api_version_header_matcher(request):
            return "Accept" in request.headers and request.headers[
                "Accept"
            ] == "application/json; version={}".format(truework.API_VERSION)

        mock.get(
            "{}{}".format(Company.url(), "?offset=0&limit=25&q=International"),
            status_code=200,
            json=self.load_fixture("company/search_manual_pagination.json"),
            additional_matcher=api_version_header_matcher,
        )

        Company.search("International")

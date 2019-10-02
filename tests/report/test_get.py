import cattr
import requests_mock
from unittest import TestCase

from tests.utils import FixtureLoader
from truework.base import APIClient, TrueworkHTTPError
from truework.report import Report
from truework import BASE_URL


class TestReportGet(TestCase, FixtureLoader):
    @requests_mock.mock()
    def test_get_success(self, mock):
        report_response = self.load_fixture("report/report_1.json")
        mock.get(
            "{}verification-requests/{}/report/".format(BASE_URL, "report_1"),
            status_code=200,
            json=report_response,
        )

        retrieve_response = Report.retrieve("report_1")
        self.assertEqual(retrieve_response, cattr.structure(report_response, Report))

    @requests_mock.mock()
    def test_get_failure(self, mock):
        mock.get(
            "{}verification-requests/{}/report/".format(BASE_URL, "report_1"),
            status_code=404,
            json={"error": {"message": "invalid id"}},
        )

        with self.assertRaises(TrueworkHTTPError) as context:
            Report.retrieve("report_1")

        self.assertEqual(context.exception.status_code, 404)

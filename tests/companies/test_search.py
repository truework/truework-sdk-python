import unittest
import requests_mock

from tests.utils import FixtureLoader
from truework.company import Company


class TestCompanySearch(unittest.TestCase, FixtureLoader):
    @requests_mock.mock()
    def test_manual_pagination(self, mock):
        mock.get(
            "{}{}".format(Company.url(), "?q=International&offset=1&limit=3"),
            status_code=200,
            json=self.load_fixture("company/search_manual_pagination.json"),
        )

        response = Company.search("International", offset=1, limit=3)
        results = list(response.results)
        self.assertEqual(len(results), 3)
        self.assertEqual(
            results[0],
            Company(
                id="745",
                name="International Academy of Design and Technology",
                domain="iadt.edu",
            ),
        )

    def _mocks_for_auto_pagination(self, mock):
        mock.get(
            "{}{}".format(Company.url(), "?q=International&offset=0&limit=2"),
            status_code=200,
            json=self.load_fixture("company/search_auto_paginate_page1.json"),
        )
        mock.get(
            "{}{}".format(Company.url(), "?q=International&offset=2&limit=2"),
            status_code=200,
            json=self.load_fixture("company/search_auto_paginate_page2.json"),
        )
        mock.get(
            "{}{}".format(Company.url(), "?q=International&offset=4&limit=2"),
            status_code=200,
            json=self.load_fixture("company/search_auto_paginate_page3.json"),
        )

    PAGE_TO_SEARCH_RESULTS = {
        1: [
            Company(
                id="745",
                name="International Academy of Design and Technology",
                domain="iadt.edu",
            ),
            Company(
                id="17756", name="International Arbitration", domain="arbitration.org"
            ),
        ],
        2: [
            Company(
                id="18729",
                name="International Association of Bomb Technicians & Investigators",
                domain="iabti.org",
            ),
            Company(
                id="12241",
                name="International Brotherhood of Boilermakers",
                domain=None,
            ),
        ],
        3: [Company(id="8267", name="International Coach Federation", domain=None)],
    }

    @requests_mock.mock()
    def test_auto_pagination(self, mock):
        self._mocks_for_auto_pagination(mock)

        response = Company.search("International", offset=0, limit=2).auto_paginate()
        self.assertEqual(len(response), 5)

        actual_results = [company for company in response]
        self.assertEqual(
            actual_results,
            self.PAGE_TO_SEARCH_RESULTS[1]
            + self.PAGE_TO_SEARCH_RESULTS[2]
            + self.PAGE_TO_SEARCH_RESULTS[3],
        )

    @requests_mock.mock()
    def test_auto_pagination_with_offset(self, mock):
        self._mocks_for_auto_pagination(mock)

        response = Company.search("International", offset=2, limit=2).auto_paginate()
        self.assertEqual(len(response), 3)

        actual_results = [company for company in response]

        self.assertEqual(len(response), 3)
        self.assertEqual(
            actual_results,
            self.PAGE_TO_SEARCH_RESULTS[2] + self.PAGE_TO_SEARCH_RESULTS[3],
        )

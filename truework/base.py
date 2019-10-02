import json
import sys

import cattr
import requests

from truework import version


class TrueworkHTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return "Status code: {} Message: {}".format(self.status_code, self.message)


class APIClient(object):
    @property
    def _user_agent(self):
        return "Truework Python SDK {}, sys.platform {}, sys.version {}".format(
            version.VERSION, sys.platform, sys.version.replace("\n", "_")
        )

    @property
    def headers(self):
        from truework import API_TOKEN, API_VERSION

        return {
            "Authorization": "Bearer {}".format(API_TOKEN),
            "User-Agent": self._user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json; version={}".format(API_VERSION),
        }

    def _raise_for_http_status(self, response):
        if 400 <= response.status_code < 600:
            try:
                msg = json.dumps(response.json().get("error", {}))
            except ValueError:
                msg = str(response.text)

            raise TrueworkHTTPError(response.status_code, msg)

    def _url(self, endpoint):
        from truework import BASE_URL

        return "{}{}".format(BASE_URL, endpoint)

    def get_url(self, url, params):
        response = requests.get(url, params, headers=self.headers)

        self._raise_for_http_status(response)

        return response.json()

    def get(self, endpoint, params):
        return self.get_url(self._url(endpoint), params)

    def post(self, endpoint, **data):
        response = requests.post(self._url(endpoint), json=data, headers=self.headers)

        self._raise_for_http_status(response)

        return response.json()


class APIResource(object):
    """
    Represents an API resource. A subclass will contain both the attributes of an instance of a resource
    and will expose functions to interact with the API for that resource.
    """

    PATH = None

    @classmethod
    def url(cls):
        from truework import BASE_URL

        return "{}{}".format(BASE_URL, cls.PATH)


class CreatableAPIResource(APIResource):
    @classmethod
    def create(cls, **data):
        """
        Creates a resource at a given endpoint
        :param data: A dictionary of key/value pairs to create the resource
        :return: An APIResource representation of the created resource
        """

        response_json = APIClient().post(cls.PATH, **data)
        return cattr.structure(response_json, cls)


class RetrievableAPIResource(APIResource):
    @classmethod
    def url_with_id(cls, id):
        return "{}{}/".format(cls.url(), id)

    @classmethod
    def retrieve(cls, id):
        """
        Retrieves a resource at a given endpoint
        :param id: The id of the resource
        :return: A subclass instance of APIResource
        """

        url = cls.url_with_id(id)
        response = APIClient().get_url(url, {})

        return cattr.structure(response, cls)


class ListableAPIResource(APIResource):
    @classmethod
    def list(cls, offset=0, limit=25):
        """
        Lists resources at a given endpoint
        :param limit: The max number of items in the page of results
        :param offset: The offset to being the listing at
        :return: An object of class `IterableAPIResponse`
        """
        query_params = {"offset": offset, "limit": limit}

        response = APIClient().get(cls.PATH, query_params)
        return IterableAPIResponse(response, cls, query_params)


class SearchableAPIResource(ListableAPIResource):
    @classmethod
    def search(cls, query=None, offset=0, limit=25):
        """
        Searches for a resource at a given endpoint
        :param query: The query string to search for
        :param limit: The max number of items in the page of results
        :param offset: The offset to begin the listing at
        :param auto_paginate: Whether to auto paginate results or not
        :return: An object of class `IterableAPIResponse`
        """
        query_params = {"offset": offset, "limit": limit}

        if query:
            query_params["q"] = query

        response = APIClient().get(cls.PATH, query_params)
        return IterableAPIResponse(response, cls, query_params)


class APIResponse(object):
    """
    This contains status, data, and converted objects.
    """

    def __init__(self, raw_response, resource_cls):
        self.raw_response = raw_response
        self._resource_cls = resource_cls
        self.results = None


class IterableAPIResponse(APIResponse):
    def __init__(self, raw_response, resource_cls, request_params):
        super(IterableAPIResponse, self).__init__(raw_response, resource_cls)
        self.results = [
            cattr.structure(result, self._resource_cls)
            for result in self.raw_response["results"]
        ]
        self.next_url = self.raw_response.get("next")
        self.num_results = raw_response.get("count")
        self.request_params = request_params

    def __iter__(self):
        for item in self.results:
            yield item

    def __len__(self):
        return len(self.results)

    def next_page(self):
        if not self.next_url:
            return None
        return IterableAPIResponse(
            APIClient().get_url(self.next_url, {}), self._resource_cls, {}
        )

    def auto_paginate(self):
        return AutoPaginatedAPIResponse(self)


class AutoPaginatedAPIResponse(object):
    def __init__(self, initial_iterable_api_response):
        self.current_response = initial_iterable_api_response
        self.num_results = initial_iterable_api_response.raw_response.get(
            "count"
        ) - initial_iterable_api_response.request_params.get("offset")

    def __iter__(self):
        while self.current_response:
            for item in self.current_response:
                yield item
            self.current_response = self.current_response.next_page()

    def __len__(self):
        return self.num_results

""" Python api for Rehive """
import os
import requests
import logging
from json.decoder import JSONDecodeError

from .exception import APIException, Timeout

API_ENDPOINT = os.environ.get("REHIVE_API_URL",
                              "https://api.rehive.com/3/")
API_STAGING_ENDPOINT = os.environ.get("API_STAGING_ENDPOINT",
                                      "https://api.staging.rehive.com/3/")


class Client:
    """
    Interface for interacting with the rehive api
    """

    def __init__(self,
                 token=None,
                 connection_pool_size=0,
                 network='live',
                 debug=False,
                 api_endpoint_url=None,
                 timeout=30,
                 user_agent=None,
                 **kwargs):

        self.token = token
        self.user_agent = user_agent
        if api_endpoint_url:
            # Override the defaults
            self.endpoint = api_endpoint_url
        else:
            self.endpoint = API_ENDPOINT if (network == 'live') else API_STAGING_ENDPOINT
        self._connection_pool_size = connection_pool_size
        self._session = None
        self.timeout = timeout

        # Enable requests logging
        if debug:
            try:
                from http.client import HTTPConnection
            except ImportError:
                from httplib import HTTPConnection
            HTTPConnection.debuglevel = 1

            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def post(self, path, data, json=True, **kwargs):
        return self._request('post', path, data, json=json, **kwargs)

    def get(self, path, **kwargs):
        return self._request('get', path, **kwargs)

    def put(self, path, data, **kwargs):
        return self._request('put', path, data, **kwargs)

    def patch(self, path, data, **kwargs):
        return self._request('patch', path, data, **kwargs)

    def delete(self, path, data, **kwargs):
        return self._request('delete', path, **kwargs)

    def options(self, path, **kwargs):
        return self._request('options', path, **kwargs)

    def _create_session(self):
        self._session = requests.Session()
        if self._connection_pool_size > 0:
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=self._connection_pool_size,
                pool_maxsize=self._connection_pool_size
            )
            self._session.mount('http://', adapter)
            self._session.mount('https://', adapter)

    def _request(self,
                 method,
                 path,
                 data=None,
                 json=True,
                 headers=None,
                 idempotent_key=None,
                 **kwargs):
        if self._session is None:
            self._create_session()

        url = self.endpoint + path
        headers = self._get_headers(
            headers=headers,
            json=json,
            idempotent_key=idempotent_key
        )
        if not kwargs.get('timeout', None):
            kwargs['timeout'] = self.timeout

        try:
            if (data and json):
                result = self._session.request(method,
                                               url,
                                               headers=headers,
                                               json=data,
                                               **kwargs)
            elif (data and not json):
                result = self._session.request(method,
                                               url,
                                               headers=headers,
                                               data=data,
                                               **kwargs)
            else:
                result = self._session.request(
                    method,
                    url,
                    headers=headers,
                    **kwargs
                )

            if not result.ok:
                if result.status_code == 404:
                    raise APIException('Not found: ' + url, result.status_code)
                if result.status_code == 500:
                    raise APIException('Internal server error: ' + url, result.status_code)
                try:
                    error_data = result.json()
                    raise APIException(error_data.get(
                            'message', 'General error'),
                            result.status_code, error_data)
                except JSONDecodeError:
                    APIException(
                        'JSON Decode error',
                        result.status_code
                    )

            response_json = self._handle_result(result)
            return response_json

        except requests.exceptions.Timeout as e:
            raise Timeout(str(e))
        except requests.exceptions.ConnectTimeout as e:
            raise Timeout(str(e))
        except requests.exceptions.ConnectionError as e:
            raise APIException(str(e))
        except requests.exceptions.RequestException as e:
            raise APIException("General request error",  None, str(e))

    def _handle_result(self, result):
        json = result.json()

        # Check for token in response and set it for the current object
        if (json and 'data' in json and 'token' in json['data']):
            self.token = json['data']['token']

        return json

    def _get_headers(self, headers=None, json=True, idempotent_key=None):
        if headers is None:
            headers = {}
        if json:
            headers['Content-Type'] = 'application/json'
        if self.token is not None:
            headers['Authorization'] = 'Token ' + str(self.token)
        if idempotent_key is not None:
            headers['Idempotency-Key'] = idempotent_key
        if self.user_agent:
            headers['User-Agent'] = str(self.user_agent)

        return headers

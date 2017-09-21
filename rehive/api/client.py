""" Python api for Rehive """
import os
import requests
import json

from .exception import APIException


class Client:
    """
    Interface for interacting with the rehive api
    """
    API_ENDPOINT = os.environ.get("REHIVE_API_URL",
                                  "https://rehive.com/api/3/")

    def __init__(self,
                 token=None,
                 connection_pool_size=0,
                 api_endpoint_url=API_ENDPOINT):

        self.token = token
        self.endpoint = api_endpoint_url
        self._connection_pool_size = connection_pool_size
        self._session = None

    def post(self, path, data):
        return self._request('post', path, data)

    def get(self, path):
        return self._request('get', path)

    def put(self, path, data):
        return self._request('put', path, data)

    def patch(self, path, data):
        return self._request('patch', path, data)

    def delete(self, path, data):
        return self._request('delete', path)

    def _create_session(self):
        self._session = requests.Session()
        if self._connection_pool_size > 0:
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=self._connection_pool_size,
                pool_maxsize=self._connection_pool_size
            )
            self._session.mount('http://', adapter)
            self._session.mount('https://', adapter)

    def _request(self, method, path, data=None):
        if self._session is None:
            self._create_session()

        url = self.endpoint + path
        headers = self._get_headers()

        try:
            if data:
                try:
                    data = json.dumps(data)
                except:
                    raise
                result = self._session.request(method,
                                               url,
                                               headers=headers,
                                               data=data)
            else:
                result = self._session.request(method, url, headers=headers)

            if not result.ok:
                if result.status_code == 404:
                    raise APIException('Not found: ' + url, result.status_code)
                error_data = result.json()
                raise APIException(error_data.get(
                        'message', 'General error'),
                        result.status_code, error_data)

            response_json = self._handle_result(result)
            return response_json

        except requests.exceptions.ConnectionError as e:
            raise APIException(str(e))
        except requests.exceptions.Timeout as e:
            raise APIException("Connection timed out.", None, str(e))
        except requests.exceptions.RequestException as e:
            raise APIException("General request error",  None, str(e))

    def _handle_result(self, result):
        json = result.json()

        # Check for token in response and set it for the current object
        if (json and 'data' in json and 'token' in json['data']):
            self.token = json['data']['token']

        return json

    def _get_headers(self):
        headers = {}
        headers['Content-Type'] = 'application/json'
        if self.token is not None:
            headers['Authorization'] = 'Token ' + str(self.token)

        return headers

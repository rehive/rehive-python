import re
from io import BufferedReader

import copy
from urllib.parse import urlparse
from urllib.parse import urljoin
import urllib.parse
from rehive.api.exception import NoNextException, NoPreviousException


class Resource(object):
    def __init__(self, client, endpoint, filters=None):
        self.client = client
        self.endpoint = endpoint + self.get_resource_name() + '/'
        self.filters = filters
        self.resource_identifier = ''
        self.has_been_hydrated = False

    def get(self, resource_id=None, timeout=None, **kwargs):
        url = self._build_url(resource_id, **kwargs)
        response = self.client.get(url, timeout=timeout)
        return self._handle_resource_data(response)

    def post(self, data=None, resource_id=None, idempotent_key=None, timeout=None, **kwargs):
        # Allow us to parse through arbitrary request arguments
        if data is None:
            data = {}

        data, files = self._handle_file_data(**data, **kwargs)
        # We need this flag to force non-json on file uploads
        json = not bool(files) if data.get('json') is None else data.pop('json')
        url = self._build_url(resource_id)
        response = self.client.post(
            url,
            data,
            json=json,
            idempotent_key=idempotent_key,
            timeout=timeout,
            files=files
        )
        return self._handle_resource_data(response)

    def put(self, resource_id='', idempotent_key=None, timeout=None, **kwargs):
        url = self._build_url(resource_id)
        data, files = self._handle_file_data(**kwargs)
        # We need this flag to force non-json on file uploads
        json = not bool(files) if data.get('json') is None else data.pop('json')
        response = self.client.put(
            url,
            data,
            json=json,
            idempotent_key=idempotent_key,
            timeout=timeout,
            files=files
        )
        return self._handle_resource_data(response)

    def patch(self, resource_id='', idempotent_key=None, timeout=None, **kwargs):
        url = self._build_url(resource_id)
        data, files = self._handle_file_data(**kwargs)
        # We need this flag to force non-json on file uploads
        json = not bool(files) if data.get('json') is None else data.pop('json')
        response = self.client.patch(
            url,
            data,
            json=json,
            idempotent_key=idempotent_key,
            timeout=timeout,
            files=files
        )
        return self._handle_resource_data(response)

    def delete(self, resource_id='', timeout=None, **kwargs):
        data = kwargs
        url = self._build_url(resource_id)
        response = self.client.delete(url, data, timeout=timeout)
        return self._handle_resource_data(response)

    def options(self, resource_id='', timeout=None, **kwargs):
        url = self._build_url(resource_id)
        response = self.client.options(url, timeout=timeout)
        return self._handle_resource_data(response)

    def update(self, resource_id='', idempotent_key=None, timeout=None, **kwargs):
        return self.patch(
            resource_id,
            idempotent_key=idempotent_key,
            timeout=timeout,
            **kwargs
        )

    def create(self, idempotent_key=None, timeout=None, **kwargs):
        return self.post(
            idempotent_key=idempotent_key,
            timeout=timeout,
            **kwargs
        )

    # PRIVATE METHODS
    def _build_url(self, resource_id=None, **kwargs):
        # currently pagination should override all
        if kwargs.get('pagination'):
            endpoint = urllib.parse.urljoin(self.endpoint, kwargs.get('pagination'))
        else:
            if resource_id:
                endpoint = urllib.parse.urljoin(
                    self.endpoint, resource_id
                )
            else:
                endpoint = self.endpoint
            endpoint = self._append_trailing_slash(endpoint)
            if (self.resource_identifier is not None):
                endpoint = urllib.parse.urljoin(
                    endpoint, self.resource_identifier
                )
            endpoint = self._append_trailing_slash(endpoint)
        if kwargs.get('filters'):
            filters = kwargs.get('filters')
            filters_clean = {}

            # Filter out any special case filters
            array_type_filters = {}
            for f in filters:
                if type(filters[f]) is list:
                    array_type_filters[f] = filters[f]
                else:
                    filters_clean[f] = filters[f]

            array_filters_string = ''
            for array_filter in array_type_filters:
                encoded_array = urllib.parse.urlencode(
                    {array_filter: array_type_filters[array_filter]},
                    safe="[],'\""
                )
                array_filters_string = re.sub('[\[\'\]\+]', '', encoded_array)

            filters_string = urllib.parse.urlencode(filters_clean)
            if filters_string:
                filters_string = filters_string + '&' + array_filters_string
            else:
                filters_string = array_filters_string

            if "?" not in endpoint:
                endpoint = endpoint + '?' + filters_string
            else:
                endpoint = endpoint + '&' + filters_string
        return endpoint

    def _put_or_patch_by_identifier(self,
                                    method,
                                    identifier,
                                    identifier_field,
                                    **kwargs):
        if (identifier is not None and identifier_field is not None):
            resource_id = '?' + identifier_field + '=' + identifier
        else:
            raise Exception('No identifier supplied')
        data = kwargs
        url = self._build_url(resource_id)
        if method == 'PATCH':
            response = self.client.patch(url, data)
        elif method == 'PUT':
            response = self.client.put(url, data)
        else:
            raise Exception('No method supplied')
        return response

    def _append_trailing_slash(self, url):
        if (re.search(r'\/+$', url) is None):
            url = url + '/'
        return url

    def _set_resource_identifier(self, resource_identifiter):
        self.resource_identifier = str(resource_identifiter)

    def _set_endpoint(self, endpoint):
        self.endpoint = self._append_trailing_slash(endpoint)

    def get_resource_name(cls):
        raise NotImplementedError(
            'The resource should define its own string name'
        )

    def _handle_resource_data(self, response):
        return_data = response
        if 'data' in response:
            return_data = response.get('data')
        self.has_been_hydrated = True

        return return_data

    def _handle_file_data(self, **kwargs):
        data = {}
        files = {}
        for key, val in kwargs.items():
            if isinstance(val, BufferedReader):
                files[key] = val
            else:
                data[key] = val

        return data, files


class ResourceList(Resource):

    def __init__(self, client, endpoint, filters=None):
        super(ResourceList, self).__init__(client, endpoint, filters)
        self.next = None
        self.previous = None
        self._count = 0

    def get(self, endpoint=None, **kwargs):
        if endpoint:
            endpoint = str(endpoint)
        url = self._build_url(endpoint, **kwargs)
        response = self.client.get(url)
        return self._handle_pagination_data(response)

    def get_next(self, **kwargs):
        if self.next is None:
            raise NoNextException
        url = self._build_url(pagination=self.next, **kwargs)
        response = self.client.get(url)
        return self._handle_pagination_data(response)

    def get_previous(self, **kwargs):
        if self.previous is None:
            raise NoPreviousException
        url = self._build_url(pagination=self.previous, **kwargs)
        response = self.client.get(url)
        return self._handle_pagination_data(response)

    @property
    def count(self):
        if (self.has_been_hydrated is False):
            self.get()
        return self._count

    # PRIVATE METHODS
    def _handle_pagination_data(self, response):
        data = response.get('data')
        return_data = data
        if 'next' in data:
            if data.get('next') is not None:
                self.next = self._get_next_page_filter(data.get('next'))
            else:
                self.next = None
        if 'previous' in data:
            if data.get('previous') is not None:
                self.previous = self._get_next_page_filter(data['previous'])
            else:
                self.previous = None
        if 'count' in data:
            self._count = data.get('count')
        if 'results' in data:
            return_data = data.get('results')
        self.has_been_hydrated = True
        return return_data

    def _get_next_page_filter(self, string):
        url_segments = string.split('/')
        last_segment = url_segments[-1]
        return last_segment

    def _build_pagination_url(self, pagination, resource_id=None):
        endpoint = self.endpoint + resource_id if resource_id else self.endpoint
        paginatated_endpoint = endpoint + pagination
        if self.filters:
            paginatated_endpoint = paginatated_endpoint + self.filters
        return paginatated_endpoint


class ResourceCollection(object):

    def __init__(self):
        self.create_resources(self.resources)

    def create_resources(self, resources):
        for resource in resources:
            setattr(self,
                    self._sanitize_resource_name(
                        resource.get_resource_name()),
                    resource(self.client, self.endpoint))

    def obj(self, resource_identifiter):
        return self.object(resource_identifiter)

    def object(self, resource_identifiter):
        resource_object = copy.copy(self)
        resource_object._set_resource_identifier(resource_identifiter)
        resource_object._set_endpoint(resource_object.endpoint + resource_object.resource_identifier)
        resource_object.create_resources(resource_object.resources)
        return resource_object

    def _sanitize_resource_name(self, string):
        return string.replace('-', '_')

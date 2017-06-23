import re
import copy


class Resource(object):
    def __init__(self, client, endpoint, filters=None):
        self.client = client
        self.endpoint = endpoint + self.get_resource_name() + '/'
        self.filters = filters
        self.resource_identifier = ''

    def get(self, function=None):
        url = self._build_url(function)
        response = self.client.get(url)
        return response

    def post(self, data={}, function=None, **kwargs):
        data = {**data, **kwargs}
        url = self._build_url(function)
        response = self.client.post(url, data)
        return response

    def put(self, function='', **kwargs):
        data = kwargs
        url = self._build_url(function)
        return self.client.put(url, data)

    def patch(self, function='', **kwargs):
        data = kwargs
        url = self._build_url(function)
        return self.client.patch(url, data)

    def create(self, **kwargs):
        self.post(**kwargs)

    # PRIVATE METHODS
    def _build_url(self, function=None):
        endpoint = self.endpoint + function if function else self.endpoint
        endpoint = self._append_trailing_slash(endpoint)
        if (self.resource_identifier is not None):
            endpoint = endpoint + self.resource_identifier
        endpoint = self._append_trailing_slash(endpoint)
        url = endpoint + self.filters if self.filters else endpoint
        return url

    def _put_or_patch_by_identifier(self,
                                    method,
                                    identifier,
                                    identifier_field,
                                    **kwargs):
        if (identifier is not None and identifier_field is not None):
            function = '?' + identifier_field + '=' + identifier
        else:
            raise Exception('No identifier supplied')
        data = kwargs
        url = self._build_url(function)
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
        self.resource_identifier = resource_identifiter

    def _set_endpoint(self, endpoint):
        self.endpoint = self._append_trailing_slash(endpoint)

    def get_resource_name(cls):
        raise NotImplementedError(
            'The resource should define its own string name'
        )


class ResourceList(Resource):

    def __init__(self, client, endpoint, filters=None):
        super(ResourceList, self).__init__(client, endpoint, filters)
        self.next = None
        self.previous = None
        self.count = 0

    def get(self, endpoint=None):
        response = super().get(endpoint)
        self._set_pagination(response)
        return response

    def get_next(self):
        url = self._build_pagination_url(self.next)
        response = self.client.get(url)
        self._set_pagination(response)
        return response

    def get_previous(self):
        url = self._build_pagination_url(self.previous)
        response = self.client.get(url)
        self._set_pagination(response)
        return response

    # PRIVATE METHODS
    def _set_pagination(self, response):
        data = response.get('data')
        if 'next' in data:
            if data.get('next') is not None:
                self.next = self._get_next_page_filter(data.get('next'))
            else:
                self.next = data.get('next')
        if 'previous' in data:
            if data.get('previous') is not None:
                self.previous = self._get_next_page_filter(data['previous'])
            else:
                self.previous = data.get('previous')
        if 'count' in data:
            self.count = data.get('count')

    def _get_next_page_filter(self, string):
        url_segments = string.split('/')
        last_segment = url_segments[-1]
        return last_segment

    def _build_pagination_url(self, pagination, function=None):
        endpoint = self.endpoint + function if function else self.endpoint
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
                    resource.get_resource_name(),
                    resource(self.client, self.endpoint))

    # Stop gap solution for my current single object problem
    def obj(self, resource_identifiter):
        return self.object(resource_identifiter)

    def object(self, resource_identifiter):
        resource_object = copy.copy(self)
        resource_object._set_resource_identifier(resource_identifiter)
        resource_object._set_endpoint(resource_object.endpoint + resource_object.resource_identifier)
        resource_object.create_resources(resource_object.resources)
        return resource_object

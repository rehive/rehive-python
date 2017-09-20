import re
import copy


class Resource(object):
    def __init__(self, client, endpoint, filters=None):
        self.client = client
        self.endpoint = endpoint + self.get_resource_name() + '/'
        self.filters = filters
        self.resource_identifier = ''
        self.has_been_hydrated = False

    def get(self, function=None, **kwargs):
        url = self._build_url(function, **kwargs)
        response = self.client.get(url)
        return self._handle_resource_data(response)

    def post(self, data={}, function=None, **kwargs):
        data = {**data, **kwargs}
        url = self._build_url(function)
        response = self.client.post(url, data)
        return self._handle_resource_data(response)

    def put(self, function='', **kwargs):
        data = kwargs
        url = self._build_url(function)
        response = self.client.put(url, data)
        return self._handle_resource_data(response)

    def patch(self, function='', **kwargs):
        data = kwargs
        url = self._build_url(function)
        response = self.client.patch(url, data)
        return self._handle_resource_data(response)

    def delete(self, function='', **kwargs):
        data = kwargs
        url = self._build_url(function)
        response = self.client.delete(url, data)
        return self._handle_resource_data(response)

    def update(self, function='', **kwargs):
        return self.patch(function, **kwargs)

    def create(self, **kwargs):
        return self.post(**kwargs)

    # PRIVATE METHODS
    def _build_url(self, function=None, **kwargs):
        # currently pagination should override all
        if kwargs.get('pagination'):
            endpoint = self.endpoint + kwargs.get('pagination')
        else:
            endpoint = self.endpoint + function if function else self.endpoint
            endpoint = self._append_trailing_slash(endpoint)
            if (self.resource_identifier is not None):
                endpoint = endpoint + self.resource_identifier
            endpoint = self._append_trailing_slash(endpoint)
        if kwargs.get('filters'):
            filters = kwargs.get('filters')
            filters_string = self._build_query_filters(filters)
            endpoint = endpoint + filters_string
        return endpoint

    def _build_query_filters(self, filters_dict, start_query=True):
        filters = '?' if start_query else '&'
        for name, value in filters_dict.items():
            filters = filters + name + "=" + value + "&"
        return filters

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

    def _handle_resource_data(self, response):
        return_data = response
        if 'data' in response:
            return_data = response.get('data')
        self.has_been_hydrated = True

        return return_data


class ResourceList(Resource):

    def __init__(self, client, endpoint, filters=None):
        super(ResourceList, self).__init__(client, endpoint, filters)
        self.next = None
        self.previous = None
        self._count = 0

    def get(self, endpoint=None, **kwargs):
        url = self._build_url(endpoint, **kwargs)
        response = self.client.get(url)
        return self._handle_pagination_data(response)

    def get_next(self, **kwargs):
        url = self._build_url(pagination=self.next, **kwargs)
        response = self.client.get(url)
        return self._handle_pagination_data(response)

    def get_previous(self, **kwargs):
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
                self.next = data.get('next')
        if 'previous' in data:
            if data.get('previous') is not None:
                self.previous = self._get_next_page_filter(data['previous'])
            else:
                self.previous = data.get('previous')
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

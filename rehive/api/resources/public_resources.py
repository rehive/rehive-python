from rehive.api.resources.base_resources import ResourceList, ResourceCollection


class PublicResources(ResourceList, ResourceCollection):
    def __init__(self, client):
        self.client = client
        self.endpoint = ''
        self.resources = (
            APILegalTerms,
            APICompanies
        )
        super(PublicResources, self).__init__(client, self.endpoint)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'public'


class APIVersions(ResourceList):
    @classmethod
    def get_resource_name(cls):
        return 'versions'


class APILegalTerms(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None):
        self.resources = (APIVersions,)

        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'legal-terms'


class APIGroups(ResourceList):
    @classmethod
    def get_resource_name(cls):
        return 'groups'


class APICompanies(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None):
        self.resources = (APIGroups, APILegalTerms)

        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'companies'


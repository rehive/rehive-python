from .base_resources import Resource, ResourceCollection, ResourceList


class APIAccounts(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None, resource_identifier=None):
        self.resources = (APIAdminCurrencies,)
        super(APIAccounts, self).__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'accounts'


class APIAdminCurrencies(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminCurrencies, self).__init__(client, endpoint, filters)

    def make_active_currency(self, code):
        return self.patch(code, active=True)

    @classmethod
    def get_resource_name(cls):
        return 'currencies'

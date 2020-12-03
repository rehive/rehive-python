from .base_resources import Resource, ResourceCollection, ResourceList


class APIAccountDefinitions(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None, resource_identifier=None):
        self.resources = (APIAccountDefinitionGroups,)
        super(APIAccountDefinitions, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'account-definitions'


class APIAccountDefinitionGroups(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (APIAccountDefinitionGroupCurrencies,)
        super(APIAccountDefinitionGroups, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'groups'


class APIAccountDefinitionGroupCurrencies(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'currencies'

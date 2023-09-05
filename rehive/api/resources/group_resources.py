from .base_resources import ResourceList, ResourceCollection


class APIPermissions(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'permissions'


class APIFees(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'fees'


class APIRequirements(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'requirements'


class APILimits(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'limits'


class APIRequirementItems(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'requirement-items'


class APIRequirementSets(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIRequirementItems
        )
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'requirement-sets'


class APITiers(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIFees,
            APIRequirements,
            APILimits,
            APIRequirementSets
        )
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'tiers'


class APIGroups(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIPermissions,
            APITiers,
            APIFees,
        )
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'groups'

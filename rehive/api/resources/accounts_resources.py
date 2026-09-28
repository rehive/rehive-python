from .base_resources import Resource, ResourceCollection, ResourceList


class APIAccounts(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None, resource_identifier=None):
        self.resources = (APIAdminCurrencies,)
        super().__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'accounts'


class APIAccountFees(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'fees'


class APIAccountLimits(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'limits'


class APIAccountEffectiveFees(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'effective-fees'


class APIAccountEffectiveLimits(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'effective-limits'


class APIAdminCurrencies(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAccountFees,
            APIAccountLimits,
            APIAccountEffectiveFees,
            APIAccountEffectiveLimits,
        )
        super().__init__(client, endpoint, filters)

    def make_active_currency(self, code):
        return self.patch(code, active=True)

    @classmethod
    def get_resource_name(cls):
        return 'currencies'


class APIAccountCurrencies(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'account-currencies'


class APIStatements(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'statements'

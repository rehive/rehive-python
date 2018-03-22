from .base_resources import Resource, ResourceCollection, ResourceList


class APICompany(Resource, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None):
        self.resources = (
            APIBanks,
            APICurrencies,
            APIBankAccount,
            APIBankAccounts
        )
        super(APICompany, self).__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'company'


class APIBanks(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'bank'


class APICurrencies(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'currencies'


class APIBankAccount(Resource):

    @classmethod
    def get_resource_name(cls):
        return 'bank-account'


class APIBankAccounts(Resource):

    @classmethod
    def get_resource_name(cls):
        return 'bank-accounts'

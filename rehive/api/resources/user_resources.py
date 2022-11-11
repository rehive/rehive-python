from .base_resources import ResourceList, Resource, ResourceCollection
from .public_resources import APILegalTerms


class UserResources(Resource, ResourceCollection):

    def __init__(self, client):
        self.client = client
        self.endpoint = ''
        self.resources = (
            APIUserAddress,
            APIUserEmail,
            APIUserMobiles,
            APIBankAccounts,
            APICryptoAccounts,
            APIDocuments,
            APIDevices,
            APIDeviceApps,
            APIWalletAccounts,
            APILegalTerms
        )
        super(UserResources, self).__init__(client, self.endpoint)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'user'


class APIUserAddress(Resource):

    @classmethod
    def get_resource_name(cls):
        return 'address'


class APIUserEmail(Resource):

    def create(self, email):
        return super().create(email=email)

    def make_primary(self, email):
        return self.patch(email, primary=True)

    @classmethod
    def get_resource_name(cls):
        return 'emails'


class APIUserMobiles(Resource):

    def create(self, number):
        return super().create(number=number)

    def make_primary(self, number):
        return self.patch(number, primary=True)

    @classmethod
    def get_resource_name(cls):
        return 'mobiles'


class APIBankAccounts(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIBankAccounts, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'bank-accounts'


class APIWalletCurrencies(ResourceList):
    def create(self, currency, **kwargs):
        data = {
            "currency": currency,
            **kwargs
        }

        return super().create(**data)

    @classmethod
    def get_resource_name(cls):
        return 'currencies'


class APIWalletAccounts(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (APIWalletCurrencies,)
        super().__init__(client, endpoint, filters)

    def create(self, user, **kwargs):
        data = {'user': user, **kwargs}
        return super().create(**data)

    @classmethod
    def get_resource_name(cls):
        return 'wallet-accounts'


class APICryptoAccounts(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APICryptoAccounts, self).__init__(client, endpoint, filters)

    def create(self, address, type, **kwargs):
        return super().create(
            address=address,
            type=type,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'crypto-accounts'


class APIDocuments(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIDocuments, self).__init__(client, endpoint, filters)

    def upload(self, document_type, file, **kwargs):
        return super().create(
            document_type=document_type,
            file=file,
            json=False,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'documents'


class APIDevices(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIDeviceApps,
        )
        super(APIDevices, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'devices'


class APIDeviceApps(Resource):

    @classmethod
    def get_resource_name(cls):
        return 'apps'

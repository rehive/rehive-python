from .base_resources import ResourceList, Resource, ResourceCollection
from .helpers import flatten_files
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
        super().__init__(client, self.endpoint)
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
        super().__init__(client, endpoint, filters)

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

    def upload(self, document_type, file=None, files=None, **kwargs):
        """
        Upload a document.

        Single-file (legacy):
            upload(type_id, file=open('id.jpg', 'rb'))

        Multi-file (aligns with DocumentType.file_rules):
            upload(type_id, files=[
                {'file': open('front.jpg', 'rb'), 'label': 'front'},
                {'file': open('back.jpg',  'rb'), 'label': 'back',
                 'description': 'Back of ID'},
            ])

        Skip an optional rule position by passing None at that index:
            upload(type_id, files=[entry0, None, entry2])
        """
        if (file is None) == (files is None):
            raise ValueError(
                "Provide exactly one of `file` or `files`."
            )

        if files is not None:
            kwargs.update(flatten_files(files))
        else:
            kwargs['file'] = file

        return super().create(
            document_type=document_type,
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
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'devices'


class APIDeviceApps(Resource):

    @classmethod
    def get_resource_name(cls):
        return 'apps'

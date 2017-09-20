from .base_resources import ResourceList, Resource, ResourceCollection


class UserResources(Resource, ResourceCollection):

    def __init__(self, client):
        self.client = client
        self.endpoint = ''
        self.resources = (
            APIUserAddress,
            APIUserEmail,
            APIUserMobiles,
            APIUserNotifications,
            APIBankAccounts,
            APICryptoAccounts,
            APIDocuments
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
        return super().create(email=email)

    def make_primary(self, number):
        return self.patch(number, primary=True)

    @classmethod
    def get_resource_name(cls):
        return 'mobiles'


class APIUserNotifications(Resource):

    def enable_sms(self, id):
        return self.update(id, sms_enabled=True)

    def disable_sms(self, id):
        return self.update(id, sms_enabled=False)

    def enable_email(self, id):
        return self.update(id, email_enabled=True)

    def disable_email(self, id):
        return self.update(id, email_enabled=False)

    @classmethod
    def get_resource_name(cls):
        return 'notifications'


class APIBankAccounts(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIBankAccounts, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'bank-accounts'


class APICryptoAccounts(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APICryptoAccounts, self).__init__(client, endpoint, filters)

    def create(self, address, crypto_type, **kwargs):
        return super().create(
            address=address,
            type=crypto_type,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'crypto-accounts'


class APIDocuments(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIDocuments, self).__init__(client, endpoint, filters)

    def create(self, document_type, file, **kwargs):
        return super().create(
            document_type=document_type,
            file=file,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'documents'

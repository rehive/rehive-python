from .base_resources import ResourceList, Resource, ResourceCollection


class AdminResources(ResourceCollection):

    def __init__(self, client):
        # Api Client instance
        self.client = client
        self.endpoint = 'admin/'

        # Resources
        self.resources = (
            APIAdminUsers,
            APIAdminCurrencies,
            APIAdminTransactions,
            APIAdminAccounts,
            APIAdminCompany,
            APIAdminWebhooks,
            APIAdminSubtypes,
            APIAdminBankAccounts,
            APIAdminTiers,
            APIAdminGroups,
            APIAdminAccountDefinitions,
            APIAdminTransactionCollections,
            APIAdminExports,
            APIAdminMetrics,
            APIAdminAuth,
            APIAdminNotifications,
        )
        self.create_resources(self.resources)


class APIAdminNotifications(ResourceList):
    @classmethod
    def get_resource_name(cls):
        return 'notifications'


class APIAdminAccounts(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None, resource_identifier=None):
        self.resources = (APIAdminAccountCurrencies,)
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'accounts'


class APIAdminCurrencies(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminLimits,
            APIAdminFees,
            APIAdminBankAccounts,
            APIAdminOverview,
            APIAdminSettings,
        )
        super().__init__(client, endpoint, filters)

    def create(self, code, divisibility, **kwargs):
        data = {
            "code": code,
            "divisibility": divisibility
        }
        response = self.post(data, **kwargs)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'currencies'


class APIAdminAccountCurrencies(APIAdminCurrencies):

    def create(self, code, **kwargs):
        data = {
            "code": code
        }
        response = self.post(data, **kwargs)
        return response


class APIAdminBankAccountCurrencies(APIAdminCurrencies):

    def create(self, code, **kwargs):
        data = {
            "code": code
        }
        response = self.post(data, **kwargs)
        return response


class APIAdminUsers(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = {
            APIAdminEmails,
            APIAdminMobiles,
            APIAdminCryptoAccounts,
            APIAdminSettings,
            APIAdminDocuments,
            APIAdminAddresses,
            APIAdminOverview,
            APIAdminPermissions,
            APIAdminTokens,
            APIAdminGroups,
            APIAdminKyc,
            APIAdminDevices,
            APIAdminBankAccounts
        }
        super(APIAdminUsers, self).__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'users'


class APIAdminDocuments(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminDocuments, self).__init__(client, endpoint, filters)

    def create(self, document_type, file, **kwargs):
        return super().create(
            document_type=document_type,
            file=file,
            json=False,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'documents'


class APIAdminEmails(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminEmails, self).__init__(client, endpoint, filters)

    def create(self, user, email, **kwargs):
        data = {
            'user': user,
            'email': email
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'emails'


class APIAdminAddresses(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminAddresses, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'addresses'


class APIAdminOverview(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminOverview, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'overview'


class APIAdminMobiles(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminMobiles, self).__init__(client, endpoint, filters)

    def create(self, user, number, **kwargs):
        data = {
            'user': user,
            'number': number
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'mobiles'


class APIAdminTransactions(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = {
            APIAdminWebhooks
        }
        super(APIAdminTransactions, self).__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    def get_totals(self, **kwargs):
        response = self.get('totals/', **kwargs)
        return response

    def update(self, function='', idempotent_key=None, timeout=None, **kwargs):
        return super(APIAdminTransactions, self).patch(
            function,
            idempotent_key=idempotent_key,
            timeout=timeout,
            **kwargs
        )

    def confirm(self, tx_code, **kwargs):
        self.patch(tx_code, "complete", **kwargs)

    def fail(self, tx_code, **kwargs):
        self.patch(tx_code, "failed", **kwargs)

    def delete(self, tx_code, **kwargs):
        self.patch(tx_code, "deleted", **kwargs)

    def create_credit(self, user, amount, currency, **kwargs):
        data = {
            'user': user,
            'amount': amount,
            'currency': currency
        }
        response = self.post(data, 'credit/', **kwargs)
        return response

    def create_debit(self, user, amount, currency, **kwargs):
        data = {
            'user': user,
            'amount': amount,
            'currency': currency
        }
        response = self.post(data, 'debit/', **kwargs)
        return response

    def create_transfer(self, user, amount, recipient, currency, **kwargs):
        data = {
            'user': user,
            'amount': amount,
            'recipient': recipient,
            'currency': currency
        }
        response = self.post(data, 'transfer/', **kwargs)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'transactions'


class APIAdminTransactionCollections(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminTransactionCollections, self).__init__(client, endpoint, filters)

    def status_patch(self, collection_id, status, **kwargs):
        data = kwargs
        data['status'] = status
        return super(APIAdminTransactionCollections, self).patch(collection_id + '/', **data)

    def confirm(self, collection_id, **kwargs):
        self.status_patch(collection_id, "complete", **kwargs)

    def fail(self, collection_id, **kwargs):
        self.status_patch(collection_id, "failed", **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'transaction-collections'


class APIAdminCompany(Resource, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminSettings,
            APIAdminCompanyAddress,
        )
        super(APIAdminCompany, self).__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'company'


class APIAdminSettings(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminSettings, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'settings'


class APIAdminKyc(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminKyc, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'kyc'


class APIAdminWebhooks(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminWebhooks, self).__init__(client, endpoint, filters)

    def create(self, url, **kwargs):
        data = {
            'url': url
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'webhooks'


class APIAdminWebhookTasks(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (APIAdminWebhookRequests,)
        super(APIAdminWebhookTasks, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'webhook-tasks'


class APIAdminWebhookRequests(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminWebhookRequests, self).__init__(
            client, endpoint, filters
        )

    @classmethod
    def get_resource_name(cls):
        return 'requests'


class APIAdminTransactionWebhooks(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminTransactionWebhooks, self).__init__(client, endpoint, filters)

    def create(self, tx_type, url, **kwargs):
        data = {
            'tx_type': tx_type,
            'url': url
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'transactions'


class APIAdminSubtypes(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminSubtypes, self).__init__(client, endpoint, filters)

    def create(self, name, tx_type, **kwargs):
        data = {
            'name': name,
            'tx_type': tx_type
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'subtypes'


class APIAdminBankAccounts(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (APIAdminBankAccountCurrencies,)
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'bank-accounts'


class APIAdminLimits(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminLimits, self).__init__(client, endpoint, filters)

    def create(self, value, limit_type, tx_type, **kwargs):
        data = {
            'value': value,
            'type': limit_type,
            'tx_type': tx_type
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'limits'


class APIAdminFees(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminFees, self).__init__(client, endpoint, filters)

    def create(self, tx_type, **kwargs):
        data = {
            'tx_type': tx_type
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'fees'


class APIAdminTiers(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminFees,
            APIAdminRequirements,
            APIAdminLimits
        )
        super(APIAdminTiers, self).__init__(client, endpoint, filters)

    def create(self, currency, **kwargs):
        data = {
            'currency': currency
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'tiers'


class APIAdminRequirements(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminRequirements, self).__init__(client, endpoint, filters)

    def create(self, requirement, **kwargs):
        data = {
            'requirement': requirement
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'requirements'


class APIAdminCryptoAccounts(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminCryptoAccounts, self).__init__(client, endpoint, filters)

    def create(self, address, crypto_type, **kwargs):
        return super().create(
            address=address,
            type=crypto_type,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'crypto-accounts'


class APIAdminPermissions(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminPermissions, self).__init__(client, endpoint, filters)

    def create(self, type, level, **kwargs):
        return super().create(
            type=type,
            level=level,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'permissions'


class APIAdminGroups(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminPermissions,
            APIAdminTiers,
        )
        super(APIAdminGroups, self).__init__(client, endpoint, filters)

    def create(self, name, **kwargs):
        data = {
            'name': name
        }
        return self.post(data, **kwargs)

    def assign(self, group, **kwargs):
        data = {
            'group': group
        }
        return self.post(data, **kwargs)

    def unassign(self, name, **kwargs):
        return self.delete(function=name, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'groups'


class APIAdminTokens(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminTokens, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'tokens'


class APIAdminAccountDefinitions(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminAccountDefinitionGroups,
        )
        super(APIAdminAccountDefinitions, self).__init__(
            client, endpoint, filters
        )

    def create(self, name, **kwargs):
        data = {
            'name': name
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'account-definitions'


class APIAdminAccountDefinitionGroups(
        ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminAccountDefinitionGroupCurrencies,
        )
        super(APIAdminAccountDefinitionGroups, self).__init__(
            client, endpoint, filters
        )

    def create(self, group, **kwargs):
        data = {
            "group": group
        }
        response = self.post(data, **kwargs)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'groups'


class APIAdminAccountDefinitionGroupCurrencies(
        ResourceList, ResourceCollection):

    def create(self, currency, **kwargs):
        data = {
            "currency": currency
        }
        response = self.post(data, **kwargs)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'currencies'


class APIAdminDevices(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminDeviceApps,
        )
        super(APIAdminDevices, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'devices'


class APIAdminDeviceApps(ResourceList, ResourceCollection):

    @classmethod
    def get_resource_name(cls):
        return 'apps'


class APIAdminExports(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super(APIAdminExports, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'exports'


class APIAdminMetrics(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None):
        self.resources = (APIAdminMetricPoints,)
        super(APIAdminMetrics, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'metrics'


class APIAdminMetricPoints(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminMetricPoints, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'points'


class APIAdminAuth(Resource):

    @classmethod
    def get_resource_name(cls):
        return 'auth'

    def login(self, user, password, **kwargs):
        data = {
            "user": user,
            "password": password,
        }
        response = self.post(data, 'login', **kwargs)
        return response

    def register(self,
                 email,
                 password1,
                 password2,
                 **kwargs):
        data = {
           "email": email,
           "password1": password1,
           "password2": password2
        }
        response = self.post(data, 'register', **kwargs)
        return response


class APIAdminCompanyAddress(Resource):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminCompanyAddress, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'address'

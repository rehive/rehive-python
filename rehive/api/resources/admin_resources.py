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
            APIAdminSwitches,
            APIAdminTiers,
            APIAdminPermissionGroups,
        )
        self.create_resources(self.resources)


class APIAdminNotifications(ResourceList):
    @classmethod
    def get_resource_name(cls):
        return 'notifications'


class APIAdminAccounts(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None, resource_identifier=None):
        self.resources = (APIAdminCurrencies,)
        super(APIAdminAccounts, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'accounts'


class APIAdminCurrencies(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminLimits,
            APIAdminFees,
            APIGeneralSwitches,
            APIAdminBankAccounts,
            APIAdminOverview,
        )
        super(APIAdminCurrencies, self).__init__(client, endpoint, filters)

    def create(self, code, description, symbol, unit, divisibility):
        data = {
            "code": code,
            "description": description,
            "symbol": symbol,
            "unit": unit,
            "divisibility": divisibility
        }
        response = self.post(data)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'currencies'


class APIAdminUsers(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = {
            APIAdminEmails,
            APIAdminMobiles,
            APIAdminCryptoAccounts,
            APIAdminSwitches,
            APIAdminDocuments,
            APIAdminAddresses,
            APIAdminOverview,
        }
        super(APIAdminUsers, self).__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    def create(self, first_name, last_name, email, mobile_number):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "mobile_number": mobile_number
        }
        response = self.post(data)
        return response

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
            'email': email
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'mobiles'


class APIAdminTransactions(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = {
            APIAdminSwitches,
            APIAdminWebhooks
        }
        super(APIAdminTransactions, self).__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    def get_totals(self):
        response = self.get('totals/')
        return response

    def patch(self, tx_code, status, **kwargs):
        data = kwargs
        data['status'] = status
        return super(APIAdminTransactions, self).patch(tx_code + '/', **data)

    def confirm(self, tx_code, **kwargs):
        self.patch(tx_code, "complete", **kwargs)

    def fail(self, tx_code, **kwargs):
        self.patch(tx_code, "failed", **kwargs)

    def delete(self, tx_code, **kwargs):
        self.patch(tx_code, "deleted", **kwargs)

    def create_credit(self, user, amount, **kwargs):
        data = {
            'user': user,
            'amount': amount
        }
        response = self.post(data, 'credit/', **kwargs)
        return response

    def create_debit(self, user, amount, **kwargs):
        data = {
            'user': user,
            'amount': amount
        }
        response = self.post(data, 'debit/', **kwargs)
        return response

    def create_transfer(self, user, amount, recipient, **kwargs):
        data = {
            'user': user,
            'amount': amount,
            'recipient': recipient
        }
        response = self.post(data, 'transfer/', **kwargs)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'transactions'


class APIAdminCompany(Resource, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (APIGeneralSwitches,)
        super(APIAdminCompany, self).__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'company'


class APIAdminSwitches(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminSwitches, self).__init__(client, endpoint, filters)

    def create(self, switch_type, enabled=False, **kwargs):
        data = {
            'switch_type': switch_type,
            'enabled': enabled
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'switches'


class APIGeneralSwitches(APIAdminSwitches):
    def __init__(self, client, endpoint, filters=None):
        super(APIGeneralSwitches, self).__init__(client, endpoint, filters)


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


class APIAdminBankAccounts(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super(APIAdminBankAccounts, self).__init__(client, endpoint, filters)

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
            APIGeneralSwitches,
            APIAdminFees,
            APIAdminRequirements,
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


class APIAdminPermissionGroups(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminPermissions,
        )
        super(APIAdminPermissionGroups, self).__init__(client, endpoint, filters)

    def create(self, name, **kwargs):
        return super().create(
            name=name,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'permission-groups'

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
            APIAdminSearch,
            APIAdminServices,
            APIAdminLegalTerms,
            APIAdminAuthenticatorRules,
            APIAdminAccessControlRules
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

    def create(self, currency, **kwargs):
        data = {
            "currency": currency
        }
        response = self.post(data, **kwargs)
        return response


class APIAdminBankAccountCurrencies(APIAdminCurrencies):

    def create(self, currency, **kwargs):
        data = {
            "currency": currency
        }
        response = self.post(data, **kwargs)
        return response


class APIAdminWalletCurrencies(ResourceList):
    def create(self, currency, **kwargs):
        data = {
            "currency": currency,
            **kwargs
        }

        return super().create(**data)

    @classmethod
    def get_resource_name(cls):
        return 'currencies'


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
            APIAdminBankAccounts,
            APIAdminWalletAccounts
        }
        super().__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'users'


class APIAdminDocuments(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

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
        super().__init__(client, endpoint, filters)

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
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'addresses'


class APIAdminOverview(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'overview'


class APIAdminMobiles(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

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
        self.resources = (APIAdminTransactionMessages,)
        super().__init__(client, endpoint, filters)
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

    def create_credit(self, amount, currency, **kwargs):
        data = {
            'amount': amount,
            'currency': currency
        }
        response = self.post(data, 'credit/', **kwargs)
        return response

    def create_debit(self, amount, currency, **kwargs):
        data = {
            'amount': amount,
            'currency': currency
        }
        response = self.post(data, 'debit/', **kwargs)
        return response

    def create_transfer(self, amount, currency, **kwargs):
        data = {
            'amount': amount,
            'currency': currency
        }
        response = self.post(data, 'transfer/', **kwargs)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'transactions'


class APIAdminTransactionMessages(ResourceList):
    def create(self, message, **kwargs):
        return super().create(**{'message': message, **kwargs})

    @classmethod
    def get_resource_name(cls):
        return 'messages'


class APIAdminTransactionCollections(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminTransactionCollectionTransactions,
        )
        super().__init__(client, endpoint, filters)

    def status_patch(self, collection_id, status, **kwargs):
        data = kwargs
        data['status'] = status
        return super().patch(collection_id + '/', **data)

    def confirm(self, collection_id, **kwargs):
        self.status_patch(collection_id, "complete", **kwargs)

    def fail(self, collection_id, **kwargs):
        self.status_patch(collection_id, "failed", **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'transaction-collections'


class APIAdminTransactionCollectionTransactions(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'transactions'


class APIAdminCompanyLinks(ResourceList):
    @classmethod
    def get_resource_name(cls):
        return 'links'


class APIAdminCompany(Resource, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminSettings,
            APIAdminCompanyAddress,
            APIAdminCompanyLinks
        )
        super().__init__(client, endpoint, filters)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'company'


class APIAdminSettings(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'settings'


class APIAdminKyc(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'kyc'


class APIAdminWebhooks(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

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
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'webhook-tasks'


class APIAdminWebhookRequests(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'requests'


class APIAdminTransactionWebhooks(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

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
        super().__init__(client, endpoint, filters)

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


class APIAdminWalletAccounts(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (APIAdminWalletCurrencies,)
        super().__init__(client, endpoint, filters)

    def create(self, user, **kwargs):
        data = {'user': user, **kwargs}
        return super().create(**data)

    @classmethod
    def get_resource_name(cls):
        return 'wallet-accounts'


class APIAdminLimits(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    def create(self, value, type, tx_type, **kwargs):
        data = {
            'value': value,
            'type': type,
            'tx_type': tx_type
        }
        return self.post(data, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'limits'


class APIAdminFees(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    def create(self, tx_type, currency, **kwargs):
        data = {
            'tx_type': tx_type,
            'currency': currency
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
        super().__init__(client, endpoint, filters)

    def create(self, currency, **kwargs):
        return self.post(**kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'tiers'


class APIAdminRequirements(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

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


class APIAdminPermissions(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    def create(self, permissions, **kwargs):
        return super().create(
            permissions=permissions,
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
            APIAdminFees
        )
        super().__init__(client, endpoint, filters)

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
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'tokens'


class APIAdminAccountDefinitions(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint, filters=None):
        self.resources = (
            APIAdminAccountDefinitionGroups,
        )
        super().__init__(client, endpoint, filters)

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
        super().__init__(client, endpoint, filters)

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
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'devices'


class APIAdminDeviceApps(ResourceList, ResourceCollection):

    @classmethod
    def get_resource_name(cls):
        return 'apps'


class APIAdminExports(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'exports'


class APIAdminMetrics(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None):
        self.resources = (APIAdminMetricPoints,)
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'metrics'


class APIAdminMetricPoints(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

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

    def deactivate(self, user, **kwargs):
        return self.post(user=user, resource_id='deactivate', **kwargs)

    def deactivate_verify(self, key, **kwargs):
        return self.post(key=key, resource_id='deactivate/verify', **kwargs)

    def password_reset(self, user, **kwargs):
        return self.post(user=user, resource_id='password/reset', **kwargs)

    def password_reset_confirm(
            self, new_password1, new_password2, uid, token, **kwargs):
        return self.post(
            new_password1=new_password1,
            new_password2=new_password2,
            uid=uid,
            token=token,
            resource_id='password/reset/confirm'
            **kwargs
        )


class APIAdminCompanyAddress(Resource):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'address'


class APIAdminSearch(ResourceList):
    @classmethod
    def get_resource_name(cls):
        return 'search'


class APIAdminServices(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None):
        self.resources = (APIAdminPermissions,)

        super().__init__(client, endpoint, filters)

    def create(self, name, url, **kwargs):
        return super().create(name=name, url=url, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'services'


class APIAdminVersions(ResourceList):
    @classmethod
    def get_resource_name(cls):
        return 'versions'


class APIAdminLegalTerms(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None):
        self.resources = (APIAdminVersions,)

        super().__init__(client, endpoint, filters)

    def create(self, name, **kwargs):
        return super().create(name=name, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'legal-terms'


class APIAdminAuthenticatorRules(ResourceList):
    def create(self, type, durability, authenticator_types, **kwargs):
        return super().create(
            type=type,
            durability=durability,
            authenticator_types=authenticator_types,
            **kwargs
        )

    @classmethod
    def get_resource_name(cls):
        return 'authenticator-rules'


class APIAdminAccessControlRules(ResourceList):
    def create(self, action, type, value, **kwargs):
        return super().create(action=action, type=type, value=value, **kwargs)

    @classmethod
    def get_resource_name(cls):
        return 'access-control-rules'

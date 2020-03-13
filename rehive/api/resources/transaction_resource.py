from .base_resources import ResourceList


class APITransactions(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super(APITransactions, self).__init__(client, endpoint, filters)

    def get_totals(self, **kwargs):
        response = self.get('totals/', **kwargs)
        return response

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

    def create_transfer(self, amount, recipient, currency, **kwargs):
        data = {
            'amount': amount,
            'recipient': recipient,
            'currency': currency
        }
        response = self.post(data, 'transfer/', **kwargs)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'transactions'


class APITransactionCollections(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super(APITransactionCollections, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'transaction-collections'

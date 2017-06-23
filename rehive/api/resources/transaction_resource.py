from .base_resources import ResourceList


class APITransactions(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super(APITransactions, self).__init__(client, endpoint, filters)

    def get_totals(self):
        response = self.get('totals/')
        return response

    def create_credit(self, amount, **kwargs):
        data = {
            'amount': amount
        }
        response = self.post(data, 'credit/', **kwargs)
        return response

    def create_debit(self, amount, **kwargs):
        data = {
            'amount': amount
        }
        response = self.post(data, 'debit/', **kwargs)
        return response

    def create_transfer(self, amount, recipient, **kwargs):
        data = {
            'amount': amount,
            'recipient': recipient
        }
        response = self.post(data, 'transfer/', **kwargs)
        return response

    @classmethod
    def get_resource_name(cls):
        return 'transactions'

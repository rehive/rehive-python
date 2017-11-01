from .api.client import Client
from .api.resources.admin_resources import AdminResources
from .api.resources.auth_resources import AuthResources
from .api.rehive_util import RehiveUtil
from .api.resources.user_resources import UserResources
from .api.resources.transaction_resource import APITransactions
from .api.resources.accounts_resources import APIAccounts
from .api.resources.company_resources import APICompany


class Rehive:

    def __init__(self, token=None, connection_pool_size=0, **kwargs):
        # API Classes
        # Leave token blank if logging in
        self.client = Client(token, connection_pool_size, **kwargs)
        self.admin = AdminResources(self.client)
        self.auth = AuthResources(self.client)
        self.util = RehiveUtil(self.client)
        self.user = UserResources(self.client)
        self.transactions = APITransactions(self.client)
        self.accounts = APIAccounts(self.client)
        self.company = APICompany(self.client)

from .api.client import Client
from .api.resources.admin_resources import AdminResources
from .api.resources.auth_resources import AuthResources
from .api.rehive_util import RehiveUtil
from .api.resources.public_resources import PublicResources
from .api.resources.user_resources import UserResources
from .api.resources.transaction_resource import (
    APITransactions, APITransactionCollections
)
from .api.resources.accounts_resources import APIAccounts
from .api.resources.company_resources import APICompany
from .api.resources.export_resources import APIExports
from .api.resources.metric_resources import APIMetrics
from .api.resources.account_definition_resources import APIAccountDefinitions


class Rehive:

    def __init__(self, token=None, connection_pool_size=0, network="live", debug=False, **kwargs):
        # API Classes
        self.debug = debug
        self.client = Client(
            token,
            connection_pool_size,
            network,
            debug,
            **kwargs
        )
        self.admin = AdminResources(self.client)
        self.auth = AuthResources(self.client)
        self.util = RehiveUtil(self.client)
        self.user = UserResources(self.client)
        self.transactions = APITransactions(self.client)
        self.transaction_collections = APITransactionCollections(self.client)
        self.accounts = APIAccounts(self.client)
        self.account_definitions = APIAccountDefinitions(self.client)
        self.company = APICompany(self.client)
        self.exports = APIExports(self.client)
        self.metrics = APIMetrics(self.client)
        self.public = PublicResources(self.client)

from .api.client import Client
from .api.resources.admin_resources import AdminResources
from .api.resources.auth_resources import AuthResources
from .api.rehive_util import RehiveUtil


class Rehive:

    def __init__(self, token=None, connection_pool_size=0):
        # API Classes
        # Leave token blank if logging in
        self.client = Client(token, connection_pool_size)
        self.admin = AdminResources(self.client)
        self.auth = AuthResources(self.client)
        self.util = RehiveUtil(self.client)

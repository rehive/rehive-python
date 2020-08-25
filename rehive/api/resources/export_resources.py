from .base_resources import ResourceList


class APIExports(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super(APIExports, self).__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'exports'

from .base_resources import ResourceList


class APIDocumentTypes(ResourceList):
    def __init__(self, client, endpoint='', filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'document-types'

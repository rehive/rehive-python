from .base_resources import ResourceList


class APIDocumentTypes(ResourceList):

    @classmethod
    def get_resource_name(cls):
        return 'document-types'

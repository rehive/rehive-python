from .base_resources import ResourceList, ResourceCollection


class APIMetrics(ResourceList, ResourceCollection):
    def __init__(self, client, endpoint='', filters=None):
        self.resources = (APIMetricPoints,)
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'metrics'


class APIMetricPoints(ResourceList):
    def __init__(self, client, endpoint, filters=None):
        super().__init__(client, endpoint, filters)

    @classmethod
    def get_resource_name(cls):
        return 'points'

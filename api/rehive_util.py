# TODO: REDO TO MATCH THE ADMIN STRUCTURE
class RehiveUtil:
    def __init__(self, client):
        self.api = client

    def get_all_endpoints(self):
        response = self.api.get('')
        return self.api.get('')

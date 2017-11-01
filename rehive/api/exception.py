class APIException(Exception):
    def __init__(self, message, status_code=None, data=None):

        super(APIException, self).__init__(message)

        self.status_code = status_code
        if data is not None:
            self.data = data

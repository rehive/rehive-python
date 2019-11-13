class APIException(Exception):
    def __init__(self, message, status_code=None, data=None):

        super(APIException, self).__init__(message)

        self.status_code = status_code
        if data is not None:
            self.data = data


class NoPaginationException(Exception):
    def __init__(self):

        super(NoPaginationException, self).__init__()


class NoNextException(NoPaginationException):
    def __init__(self):

        super(NoNextException, self).__init__()


class NoPreviousException(NoPaginationException):
    def __init__(self):

        super(NoPreviousException, self).__init__()


class Timeout(Exception):
    def __init__(self, message):
        super(Timeout, self).__init__(message)
class APIException(Exception):
    def __init__(self, message, status_code=None, data=None):
        self.status_code = status_code
        if data is not None:
            self.data = data
            if data.get('data'):
                keys = ', '.join(
                    (
                        key for key in data['data'].keys()
                        if key != 'non_field_errors'
                    )
                )
                message = f"There is an error with {keys}. " \
                          f"Please check the data property for more details" \
                    if keys else message

        super(APIException, self).__init__(message)


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

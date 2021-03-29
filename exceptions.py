from abc import ABC


class ParameterError(Exception, ABC):
    error_code = 0
    message = ''

    def __str__(self):
        return f'E{self.error_code}: {self.message}'


class FirstNameNotFound(ParameterError):
    error_code = 1
    message = "'FirstName' is required parameter"


class LastNameNotFound(ParameterError):
    error_code = 2
    message = "'LastName' is required parameter"


class InvalidParameterType(ParameterError):
    error_code = 3
    message = 'Invalid parameter type'

    def __init__(self, field, types):
        super().__init__()
        if not isinstance(types, list):
            types = [types]
        self.message = f'Invalid type on {field}. It must be <{", ".join(types)}>'


class InvalidParameterPattern(ParameterError):
    error_code = 4
    message = 'Invalid parameter value'

    def __init__(self, field):
        super().__init__()
        self.message = f'Invalid pattern on {field}. It must be alphabetic.'


class InvalidParameterValue(ParameterError):
    error_code = 5

    def __init__(self, field, message):
        super().__init__()
        self.message = f'Invalid value on {field}. {message}'

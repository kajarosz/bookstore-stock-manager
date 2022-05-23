class GeneralException(Exception):
    pass

class RoutingException(GeneralException):
    status_code = 400

    def __init__(self, message):
        self.message = {'error': message}

class FunctionException(GeneralException):
    status_code = 400

    def __init__(self, message):
        self.message = {'error': message}

class ApiRequestException(GeneralException):
    status_code = 400

    def __init__(self, message):
        self.message = {'error': message}
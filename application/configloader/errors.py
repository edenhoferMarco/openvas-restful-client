class ConfigValidationError(Exception):
    """
        Raised if an error during json validation occured.
    """
    def __init__(self, message, prior_exception):
        self.message = message
        self.prior_exception = prior_exception

    def print(self):
        print(self.prior_exception)
        print(self.message)
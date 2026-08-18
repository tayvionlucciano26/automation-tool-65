class CustomError(Exception):
    """Base class for other exceptions."""
    pass

class InvalidInputError(CustomError):
    """Exception raised for invalid input values."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class OperationFailedError(CustomError):
    """Exception raised when an operation fails."""
    def __init__(self, operation, message):
        self.operation = operation
        self.message = message
        super().__init__(f'{operation} failed: {message}')

class ResourceNotFoundError(CustomError):
    """Exception raised when a resource is not found."""
    def __init__(self, resource):
        self.resource = resource
        self.message = f'The resource {resource} was not found.'
        super().__init__(self.message)
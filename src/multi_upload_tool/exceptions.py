class MultiUploadException(Exception):
    """Base exception for Multi Upload Tool"""
    pass

class AuthenticationError(MultiUploadException):
    """Raised when authentication fails"""
    pass

class APIError(MultiUploadException):
    """Raised when the API returns an error"""
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class ValidationError(MultiUploadException):
    """Raised when input validation fails"""
    pass

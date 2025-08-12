class ApplicationError(Exception):
    """Base class for application-specific errors."""
    pass

class ApiError(ApplicationError):
    """Custom exception for errors from the external Alpha Vantage API."""
    pass
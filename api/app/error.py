class APIError(Exception):
    """Base exception for API-specific errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ExternalServiceError(APIError):
    """Exception raised for errors when calling external services."""

    def __init__(
        self,
        service_name: str,
        detail: str = "An error occurred with an external service.",
        status_code: int = 500,
    ):
        super().__init__(f"{service_name} error: {detail}", status_code)

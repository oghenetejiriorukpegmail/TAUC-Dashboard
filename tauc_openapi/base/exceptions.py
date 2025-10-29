"""Exception classes for TAUC API."""


class TAUCApiException(Exception):
    """Base exception for TAUC API errors."""

    def __init__(self, message: str, cause: Exception = None):
        """
        Initialize TAUC API exception.

        Args:
            message: Error message
            cause: Original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.cause = cause

    def __str__(self):
        if self.cause:
            return f"{self.message} (caused by: {self.cause})"
        return self.message

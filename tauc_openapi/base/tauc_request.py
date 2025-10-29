"""Base request class for TAUC API."""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from enum import Enum


class HttpMethod(Enum):
    """HTTP methods supported by TAUC API."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class TAUCRequest(ABC):
    """
    Abstract base class for all TAUC API requests.

    All request classes should extend this class and implement the required methods.
    """

    def __init__(self):
        self._headers: Dict[str, str] = {}

    @abstractmethod
    def get_method(self) -> HttpMethod:
        """
        Get the HTTP method for this request.

        Returns:
            HttpMethod enum value
        """
        pass

    @abstractmethod
    def get_url(self) -> str:
        """
        Get the URL path for this request.

        Returns:
            URL path (e.g., "/v1/openapi/device-information/device-id")
        """
        pass

    def get_content_type(self) -> str:
        """
        Get the Content-Type header for this request.

        Returns:
            Content type string (default: "application/json; charset=UTF-8;")
        """
        return "application/json; charset=UTF-8;"

    def set_header(self, key: str, value: str) -> None:
        """
        Set a custom header for this request.

        Args:
            key: Header name
            value: Header value
        """
        if key is None or value is None:
            raise ValueError("Header key and value cannot be None")
        self._headers[key] = value

    def get_headers(self) -> Dict[str, str]:
        """
        Get all custom headers for this request.

        Returns:
            Dictionary of header key-value pairs
        """
        return self._headers.copy()

    def __str__(self) -> str:
        """String representation of the request."""
        class_name = self.__class__.__name__
        attrs = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return f"{class_name}({attrs})"

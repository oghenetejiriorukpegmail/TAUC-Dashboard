"""Base response class for TAUC API."""

from typing import Dict, Optional, Any, TypeVar, Generic
import json

T = TypeVar('T')


class TAUCResponse(Generic[T]):
    """
    Base class for all TAUC API responses.

    All response classes should extend this class.

    Attributes:
        error_code: API error code (0 for success)
        msg: Response message
        http_code: HTTP status code
        http_message: HTTP status message
        headers: Response headers
        result: Response data (type varies by endpoint)
    """

    def __init__(self, http_response=None):
        """
        Initialize TAUC response.

        Args:
            http_response: requests.Response object (optional)
        """
        self.error_code: Optional[int] = None
        self.msg: Optional[str] = None
        self.http_code: Optional[int] = None
        self.http_message: Optional[str] = None
        self.headers: Dict[str, str] = {}
        self.result: Optional[T] = None
        self._raw_json: Optional[str] = None  # Store raw JSON response

        if http_response is not None:
            self._parse_response(http_response)

    def _parse_response(self, http_response) -> None:
        """
        Parse HTTP response and populate response fields.

        Args:
            http_response: requests.Response object
        """
        self.http_code = http_response.status_code
        self.http_message = http_response.reason
        self.headers = dict(http_response.headers)

        if http_response.content:
            try:
                # Store raw JSON response text
                self._raw_json = http_response.text

                data = http_response.json()
                self.error_code = data.get("errorCode")
                self.msg = data.get("msg")

                # Parse result field if present
                if "result" in data:
                    self.result = self._parse_result(data["result"])
            except json.JSONDecodeError:
                # Response is not JSON
                pass

    def _parse_result(self, result_data: Any) -> T:
        """
        Parse the result field from response data.

        Subclasses should override this to provide custom parsing.

        Args:
            result_data: Raw result data from response

        Returns:
            Parsed result object
        """
        return result_data

    def is_success(self) -> bool:
        """
        Check if the API call was successful.

        Returns:
            True if error_code is 0, False otherwise
        """
        return self.error_code == 0

    def get_raw_json(self) -> Optional[Dict[str, Any]]:
        """
        Get the raw JSON response as a Python dict.

        Returns:
            Raw JSON response as dict, or None if not available
        """
        if self._raw_json:
            try:
                return json.loads(self._raw_json)
            except json.JSONDecodeError:
                return None
        return None

    def __str__(self) -> str:
        """String representation of the response."""
        return (
            f"{self.__class__.__name__}("
            f"error_code={self.error_code}, "
            f"msg={self.msg}, "
            f"http_code={self.http_code}, "
            f"result={self.result})"
        )

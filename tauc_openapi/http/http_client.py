"""HTTP client with mTLS support for TAUC API."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
from typing import Optional, Dict
from ..base.exceptions import TAUCApiException


class SSLAdapter(HTTPAdapter):
    """Custom HTTPAdapter to use client certificates for mTLS."""

    def __init__(self, certfile: str, keyfile: str, *args, **kwargs):
        """
        Initialize SSL adapter with client certificate.

        Args:
            certfile: Path to client certificate file
            keyfile: Path to client private key file
        """
        self.certfile = certfile
        self.keyfile = keyfile
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        """Initialize pool manager with SSL context."""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)


class HttpClient:
    """
    HTTP client for making requests to TAUC API with mTLS support.
    """

    def __init__(
        self,
        client_cert_path: str,
        client_key_path: str,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize HTTP client.

        Args:
            client_cert_path: Path to client certificate file
            client_key_path: Path to client private key file
            timeout: Request timeout in seconds (default: 30)
            verify_ssl: Whether to verify SSL certificates (default: True)
        """
        self.session = requests.Session()
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        # Mount SSL adapter for HTTPS requests
        ssl_adapter = SSLAdapter(client_cert_path, client_key_path)
        self.session.mount('https://', ssl_adapter)

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        json_data: Optional[dict] = None,
        data: Optional[str] = None
    ) -> requests.Response:
        """
        Make HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            url: Full URL
            headers: Request headers
            params: Query parameters
            json_data: JSON data for request body
            data: Raw string data for request body

        Returns:
            requests.Response object

        Raises:
            TAUCApiException: If request fails
        """
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                data=data,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            return response
        except requests.exceptions.RequestException as e:
            raise TAUCApiException(f"HTTP request failed: {url}", cause=e)

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

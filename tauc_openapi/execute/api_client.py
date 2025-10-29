"""Main API client for TAUC OpenAPI."""

from typing import Type, TypeVar, Optional
from ..base.client_type import ClientType
from ..base.tauc_request import TAUCRequest, HttpMethod
from ..base.tauc_response import TAUCResponse
from ..base.exceptions import TAUCApiException
from ..base.request_utils import RequestUtils
from ..http.http_client import HttpClient
from .auth_manager import AuthManager, AccessTokenManager

T = TypeVar('T', bound=TAUCResponse)


class ApiClient:
    """
    Main API client for TP-Link TAUC OpenAPI.

    Supports both OAuth 2.0 and Access Key/Secret Key authentication.
    All API calls require mutual TLS (mTLS) authentication.
    """

    def __init__(
        self,
        client_type: ClientType,
        domain_name: str,
        client_cert_path: str,
        client_key_path: str,
        access_key: Optional[str] = None,
        secret: Optional[str] = None,
        client_id: Optional[str] = None
    ):
        """
        Initialize API client.

        Args:
            client_type: Authentication type (ACCESS_KEY or OAUTH_TWO)
            domain_name: API domain name (e.g., "https://api.tplinkcloud.com")
            client_cert_path: Path to client certificate file
            client_key_path: Path to client private key file
            access_key: Access key (for AK/SK auth)
            secret: Secret key (for AK/SK auth)
            client_id: OAuth client ID (for OAuth 2.0)
        """
        self.client_type = client_type
        self.domain_name = self._resolve_domain_name(domain_name)
        self.client_cert_path = client_cert_path
        self.client_key_path = client_key_path
        self.access_key = access_key
        self.secret = secret
        self.client_id = client_id

        # Initialize HTTP client
        self.http_client = HttpClient(client_cert_path, client_key_path)

    @classmethod
    def build_aksk_client(
        cls,
        access_key: str,
        secret_key: str,
        domain_name: str,
        client_cert_path: str,
        client_key_path: str
    ) -> 'ApiClient':
        """
        Build API client with Access Key/Secret Key authentication.

        Args:
            access_key: Access key
            secret_key: Secret key
            domain_name: API domain name
            client_cert_path: Path to client certificate
            client_key_path: Path to client private key

        Returns:
            Configured ApiClient instance
        """
        if not all([access_key, secret_key, domain_name, client_cert_path, client_key_path]):
            raise ValueError("All parameters are required for AK/SK client")

        return cls(
            client_type=ClientType.ACCESS_KEY,
            domain_name=domain_name,
            client_cert_path=client_cert_path,
            client_key_path=client_key_path,
            access_key=access_key,
            secret=secret_key
        )

    @classmethod
    def build_oauth_client(
        cls,
        client_id: str,
        client_secret: str,
        domain_name: str,
        client_cert_path: str,
        client_key_path: str
    ) -> 'ApiClient':
        """
        Build API client with OAuth 2.0 authentication.

        Args:
            client_id: OAuth client ID
            client_secret: OAuth client secret
            domain_name: API domain name
            client_cert_path: Path to client certificate
            client_key_path: Path to client private key

        Returns:
            Configured ApiClient instance
        """
        if not all([client_id, client_secret, domain_name, client_cert_path, client_key_path]):
            raise ValueError("All parameters are required for OAuth client")

        return cls(
            client_type=ClientType.OAUTH_TWO,
            domain_name=domain_name,
            client_cert_path=client_cert_path,
            client_key_path=client_key_path,
            secret=client_secret,
            client_id=client_id
        )

    def api_call(
        self,
        request: TAUCRequest,
        response_class: Type[T],
        access_token: Optional[str] = None
    ) -> T:
        """
        Make an API call.

        Args:
            request: Request object
            response_class: Response class to instantiate
            access_token: OAuth access token (required for OAuth 2.0, optional for AK/SK)

        Returns:
            Response object of specified type

        Raises:
            TAUCApiException: If API call fails
        """
        return self._api_call_action(request, response_class, access_token, auth=True)

    def access_token_call(self, request: TAUCRequest, response_class: Type[T]) -> T:
        """
        Make an access token request (no authentication required).

        Args:
            request: Access token request object
            response_class: Response class to instantiate

        Returns:
            Response object with access token

        Raises:
            TAUCApiException: If request fails
        """
        # Populate OAuth fields if this is a GetAccessTokenRequest
        if hasattr(request, 'client_id') and hasattr(request, 'client_secret'):
            if self.client_id and self.secret:
                request.client_id = self.client_id
                request.client_secret = self.secret
                if not request.grant_type:
                    request.grant_type = "client_credentials"

        return self._api_call_action(request, response_class, access_token=None, auth=False)

    def _api_call_action(
        self,
        request: TAUCRequest,
        response_class: Type[T],
        access_token: Optional[str],
        auth: bool
    ) -> T:
        """
        Internal method to execute API call.

        Args:
            request: Request object
            response_class: Response class to instantiate
            access_token: OAuth access token (if applicable)
            auth: Whether to attach authentication headers

        Returns:
            Response object

        Raises:
            TAUCApiException: If API call fails
        """
        try:
            # Validate access token for OAuth
            if access_token is not None and self.client_type != ClientType.OAUTH_TWO:
                raise TAUCApiException("Access token provided but client is not OAuth 2.0")

            # Get request URL (without domain) for auth signature
            request_url_path = request.get_url()

            # Build full URL with path variables replaced
            full_url = self.domain_name + request_url_path
            full_url = RequestUtils.process_path_variables(full_url, request)

            # Process request URL path with variables for auth (without domain)
            request_url_for_auth = RequestUtils.process_path_variables(request_url_path, request)

            # Build request body FIRST (needed for auth signature)
            request_body_str = None
            if request.get_method() in [HttpMethod.POST, HttpMethod.PUT, HttpMethod.PATCH, HttpMethod.DELETE]:
                request_body_str = RequestUtils.process_request_body(request_url_path, request)

            # Build headers
            headers = RequestUtils.process_headers(request)

            # Attach authentication headers (pass URL and body for signature)
            if auth:
                AuthManager.attach_auth_header(
                    self.client_type,
                    headers,
                    request_url_for_auth,
                    request_body_str,
                    self.access_key,
                    self.secret,
                    access_token
                )

            # Build query parameters
            params = None
            if request.get_method() in [HttpMethod.GET, HttpMethod.POST]:
                params = RequestUtils.process_query_params(request_url_path, request)

            # Make HTTP request
            # If we have a request body string, send it as data
            # Otherwise let requests library handle JSON serialization
            http_response = self.http_client.request(
                method=request.get_method().value,
                url=full_url,
                headers=headers,
                params=params,
                json_data=None,  # We handle serialization ourselves
                data=request_body_str
            )

            # Parse response
            response = response_class(http_response)

            # Handle expired token
            if response.error_code == AuthManager.ERROR_CODE_INVALID_TOKEN:
                if self.client_id:
                    AccessTokenManager.remove_expired_token(self.client_id)

            return response

        except Exception as e:
            if isinstance(e, TAUCApiException):
                raise
            raise TAUCApiException(f"API call failed: {e}", cause=e)

    def _build_json_body(self, request: TAUCRequest) -> Optional[dict]:
        """
        Build JSON body from request object.

        Args:
            request: Request object

        Returns:
            Dictionary for JSON serialization, or None
        """
        body_dict = {}
        for attr_name in dir(request):
            if attr_name.startswith('_') or attr_name in ['get_method', 'get_url', 'get_content_type', 'set_header', 'get_headers']:
                continue

            value = getattr(request, attr_name, None)
            if value is not None and not callable(value):
                body_dict[attr_name] = value

        return body_dict if body_dict else None

    @staticmethod
    def _resolve_domain_name(domain_name: str) -> str:
        """
        Ensure domain name starts with https://.

        Args:
            domain_name: Domain name

        Returns:
            Domain name with https:// prefix
        """
        if domain_name.startswith("https://"):
            return domain_name
        return f"https://{domain_name}"

    def close(self) -> None:
        """Close HTTP client."""
        self.http_client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

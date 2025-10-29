"""Authentication management for TAUC API - CORRECTED to match Java SDK."""

import hashlib
import hmac
import base64
import time
import uuid
import json
from typing import Dict, Optional
from ..base.client_type import ClientType


class AuthManager:
    """Manages authentication headers for API requests."""

    ERROR_CODE_INVALID_TOKEN = -70435
    X_AUTH_HEADER = "X-Authorization"
    AUTH_HEADER = "Authorization"

    @staticmethod
    def attach_auth_header(
        client_type: ClientType,
        headers: Dict[str, str],
        request_url: str,
        request_body: Optional[str],
        access_key: Optional[str] = None,
        secret: Optional[str] = None,
        access_token: Optional[str] = None
    ) -> None:
        """
        Attach authentication headers to request.

        Args:
            client_type: Type of authentication (ACCESS_KEY or OAUTH_TWO)
            headers: Headers dictionary to modify
            request_url: Full request URL path (without domain)
            request_body: Serialized request body (JSON string or None)
            access_key: Access key for AK/SK authentication
            secret: Secret key for authentication
            access_token: Access token for OAuth 2.0 authentication
        """
        if client_type == ClientType.ACCESS_KEY:
            if not access_key or not secret:
                raise ValueError("Access key and secret are required for AK/SK authentication")
            x_auth = AuthManager._get_x_auth(access_key, secret, request_url, request_body)
            headers[AuthManager.X_AUTH_HEADER] = x_auth

        elif client_type == ClientType.OAUTH_TWO:
            if not access_token:
                raise ValueError("Access token is required for OAuth 2.0 authentication")
            if not secret:
                raise ValueError("Client secret is required for OAuth 2.0 authentication")

            headers[AuthManager.AUTH_HEADER] = f"Bearer {access_token}"
            # For OAuth, X-Auth doesn't include AccessKey
            x_auth = AuthManager._get_x_auth(None, secret, request_url, request_body)
            headers[AuthManager.X_AUTH_HEADER] = x_auth

    @staticmethod
    def _get_x_auth(
        access_key: Optional[str],
        secret: str,
        request_url: str,
        request_body: Optional[str]
    ) -> str:
        """
        Generate X-Authorization header value.

        Format: Nonce={uuid},AccessKey={key},Signature={signature},Timestamp={timestamp}
        (AccessKey omitted for OAuth 2.0)

        Args:
            access_key: Access key (None for OAuth 2.0)
            secret: Secret key for signing
            request_url: Request URL path
            request_body: Request body as JSON string

        Returns:
            X-Authorization header value
        """
        timestamp = int(time.time())
        nonce = str(uuid.uuid4())

        # Generate signature
        signature = AuthManager._generate_signature(
            secret, request_url, request_body, nonce, timestamp
        )

        # Build X-Authorization header
        parts = [f"Nonce={nonce}"]
        if access_key:
            parts.append(f"AccessKey={access_key}")
        parts.append(f"Signature={signature}")
        parts.append(f"Timestamp={timestamp}")

        return ",".join(parts)

    @staticmethod
    def _generate_signature(
        secret: str,
        request_url: str,
        request_body: Optional[str],
        nonce: str,
        timestamp: int
    ) -> str:
        """
        Generate signature using HMAC-SHA256.

        Signature is generated from:
        1. If body exists and is not empty or "{}":
           - ContentMD5 = Base64(MD5(body)) + "\n"
        2. Timestamp + "\n"
        3. Nonce + "\n"
        4. RequestURL

        Then signed with HMAC-SHA256 and hex encoded.

        Args:
            secret: Secret key for signing
            request_url: Request URL path
            request_body: Request body (JSON string or None)
            nonce: Random nonce
            timestamp: Unix timestamp

        Returns:
            Hex-encoded signature
        """
        parts = []

        # Add Content-MD5 if body exists and is not empty
        if request_body and request_body.strip() and request_body.strip() != "{}":
            # Normalize JSON (remove whitespace)
            try:
                normalized_body = json.dumps(json.loads(request_body), separators=(',', ':'))
            except (json.JSONDecodeError, ValueError):
                normalized_body = request_body

            # Compute MD5 and base64 encode
            md5_hash = hashlib.md5(normalized_body.encode('utf-8')).digest()
            content_md5 = base64.b64encode(md5_hash).decode('utf-8')
            parts.append(content_md5)

        # Add timestamp, nonce, and URL
        parts.append(str(timestamp))
        parts.append(nonce)
        parts.append(request_url)

        # Join with newlines
        string_to_sign = "\n".join(parts)

        # Sign with HMAC-SHA256
        signature_bytes = hmac.new(
            secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()

        # Convert to hex string
        signature_hex = signature_bytes.hex()

        return signature_hex


class AccessTokenManager:
    """Manages OAuth 2.0 access tokens."""

    # In-memory token cache (client_id -> token)
    _token_cache: Dict[str, str] = {}

    @classmethod
    def cache_token(cls, client_id: str, access_token: str) -> None:
        """
        Cache access token for client.

        Args:
            client_id: OAuth client ID
            access_token: Access token to cache
        """
        cls._token_cache[client_id] = access_token

    @classmethod
    def get_cached_token(cls, client_id: str) -> Optional[str]:
        """
        Get cached access token for client.

        Args:
            client_id: OAuth client ID

        Returns:
            Cached access token, or None if not cached
        """
        return cls._token_cache.get(client_id)

    @classmethod
    def remove_expired_token(cls, client_id: str) -> None:
        """
        Remove expired token from cache.

        Args:
            client_id: OAuth client ID
        """
        if client_id in cls._token_cache:
            del cls._token_cache[client_id]

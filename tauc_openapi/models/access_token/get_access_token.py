"""Get access token request and response models."""

from dataclasses import dataclass
from typing import Optional
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class GetAccessTokenRequest(TAUCRequest):
    """Request to get OAuth 2.0 access token."""

    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    grant_type: Optional[str] = "client_credentials"

    def __post_init__(self):
        super().__init__()

    def get_method(self) -> HttpMethod:
        return HttpMethod.POST

    def get_url(self) -> str:
        return RequestUrlCollection.GET_ACCESS_TOKEN

    def get_content_type(self) -> str:
        return "application/x-www-form-urlencoded"


@dataclass
class AccessTokenResult:
    """Access token result data."""
    access_token: Optional[str] = None
    expires_in: Optional[str] = None
    token_type: Optional[str] = None


class GetAccessTokenResponse(TAUCResponse[AccessTokenResult]):
    """Response containing access token."""

    def _parse_result(self, result_data: dict) -> AccessTokenResult:
        """Parse access token result."""
        if isinstance(result_data, dict):
            return AccessTokenResult(
                # Try both snake_case and camelCase
                access_token=result_data.get("access_token") or result_data.get("accessToken"),
                expires_in=result_data.get("expires_in") or result_data.get("expiresIn"),
                token_type=result_data.get("token_type") or result_data.get("tokenType")
            )
        return result_data

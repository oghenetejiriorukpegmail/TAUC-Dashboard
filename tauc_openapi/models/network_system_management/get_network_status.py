"""Get network status request and response models."""

from dataclasses import dataclass
from typing import Optional
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class GetNetworkStatusRequest(TAUCRequest):
    """
    Request to get network status.

    Attributes:
        networkId: Network ID (must use camelCase to match URL path variable)
    """
    networkId: Optional[str] = None

    def __init__(self, network_id: str):
        super().__init__()
        self.networkId = network_id  # Set camelCase attribute for path variable

    def get_method(self) -> HttpMethod:
        return HttpMethod.GET

    def get_url(self) -> str:
        return RequestUrlCollection.GET_NETWORK_STATUS


@dataclass
class NetworkStatusResult:
    """Network status result data."""
    status: Optional[str] = None


class GetNetworkStatusResponse(TAUCResponse[NetworkStatusResult]):
    """Response containing network status."""

    def _parse_result(self, result_data: dict) -> NetworkStatusResult:
        """Parse network status result."""
        if isinstance(result_data, dict):
            return NetworkStatusResult(status=result_data.get("status"))
        return result_data

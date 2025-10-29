"""Get network ID by network name request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class GetNetworkIdRequest(TAUCRequest):
    """
    Request to get network ID by network name.

    Attributes:
        networkName: Network name to look up
    """
    networkName: Optional[str] = None

    def __init__(self, networkName: Optional[str] = None):
        super().__init__()
        self.networkName = networkName

    def get_method(self) -> HttpMethod:
        return HttpMethod.GET

    def get_url(self) -> str:
        return RequestUrlCollection.GET_NETWORK_ID


@dataclass
class NetworkIdResult:
    """Network ID result data."""
    networkName: Optional[str] = None
    id: Optional[int] = None


class GetNetworkIdResponse(TAUCResponse[List[NetworkIdResult]]):
    """Response containing network ID(s)."""

    def _parse_result(self, result_data: dict) -> Optional[List[NetworkIdResult]]:
        """Parse network ID result list."""
        if isinstance(result_data, list):
            results = []
            for item in result_data:
                results.append(NetworkIdResult(
                    networkName=item.get("networkName"),
                    id=item.get("id")
                ))
            return results
        return None

"""Delete network list request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class DeleteNetworkListRequest(TAUCRequest):
    """
    Request to delete multiple networks.

    Attributes:
        network_ids: List of network IDs to delete
    """
    network_ids: Optional[List[int]] = None

    def __post_init__(self):
        super().__init__()

    def get_method(self) -> HttpMethod:
        return HttpMethod.DELETE

    def get_url(self) -> str:
        return RequestUrlCollection.DELETE_NETWORK_LIST


@dataclass
class DeleteNetworkListResult:
    """Delete network list result data."""
    network_id: Optional[int] = None
    error_reason: Optional[str] = None


class DeleteNetworkListResponse(TAUCResponse[List[DeleteNetworkListResult]]):
    """Response for delete network list operation."""

    def _parse_result(self, result_data) -> Optional[List[DeleteNetworkListResult]]:
        """Parse delete network list result."""
        if not result_data:
            return None

        if not isinstance(result_data, list):
            return None

        results = []
        for item in result_data:
            results.append(DeleteNetworkListResult(
                network_id=item.get("networkId"),
                error_reason=item.get("errorReason")
            ))

        return results if results else None

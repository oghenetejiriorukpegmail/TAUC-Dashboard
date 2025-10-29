"""Delete network request and response models."""

from dataclasses import dataclass
from typing import Optional
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class DeleteNetworkRequest(TAUCRequest):
    """
    Request to delete a single network.

    Attributes:
        networkId: Network ID to delete (path parameter)
    """
    networkId: Optional[int] = None

    def __post_init__(self):
        super().__init__()

    def get_method(self) -> HttpMethod:
        return HttpMethod.DELETE

    def get_url(self) -> str:
        return RequestUrlCollection.DELETE_NETWORK


class DeleteNetworkResponse(TAUCResponse[None]):
    """Response for delete network operation."""

    def _parse_result(self, result_data) -> None:
        """Parse delete network result (no result data expected)."""
        return None

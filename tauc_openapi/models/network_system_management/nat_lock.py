"""NAT lock mesh controller request and response models."""

from dataclasses import dataclass
from typing import Optional
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class NATLockMeshControllerRequest(TAUCRequest):
    """
    Request to lock NAT for a network (suspend network).

    Attributes:
        networkId: Network ID to lock (must use camelCase to match URL path variable)
    """
    networkId: Optional[str] = None

    def __init__(self, network_id: str):
        super().__init__()
        self.networkId = network_id  # Set camelCase attribute for path variable

    def get_method(self) -> HttpMethod:
        return HttpMethod.POST

    def get_url(self) -> str:
        return RequestUrlCollection.NAT_LOCK_MESH_CONTROLLER


class NATLockMeshControllerResponse(TAUCResponse):
    """Response for NAT lock operation."""
    pass

"""NAT unlock mesh controller request and response models."""

from dataclasses import dataclass
from typing import Optional
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class NATUnlockMeshControllerRequest(TAUCRequest):
    """
    Request to unlock NAT for a network (resume network).

    Attributes:
        networkId: Network ID to unlock (must use camelCase to match URL path variable)
    """
    networkId: Optional[str] = None

    def __init__(self, network_id: str):
        super().__init__()
        self.networkId = network_id  # Set camelCase attribute for path variable

    def get_method(self) -> HttpMethod:
        return HttpMethod.POST

    def get_url(self) -> str:
        return RequestUrlCollection.NAT_UNLOCK_MESH_CONTROLLER


class NATUnlockMeshControllerResponse(TAUCResponse):
    """Response for NAT unlock operation."""
    pass

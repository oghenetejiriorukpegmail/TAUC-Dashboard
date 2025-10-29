"""Batch add networks request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection
from .add_network import (
    PreConfig, MeshUnit, Tag,
    PreConfigInternet, PreConfigWireless,
    PreConfigSipUserInfo, PreConfigSipAlg
)


@dataclass
class SingleNetwork:
    """Single network configuration for batch operation."""
    network_name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    olt: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    subscribe_download: Optional[str] = None
    subscribe_upload: Optional[str] = None
    subscribe_date: Optional[str] = None
    user_network_profile_city: Optional[str] = None
    mesh_unit_list: Optional[List[MeshUnit]] = None
    tags: Optional[List[Tag]] = None
    pre_config: Optional[PreConfig] = None


@dataclass
class BatchAddingNetworksRequest(TAUCRequest):
    """
    Request to batch add multiple networks.

    Attributes:
        networks_list: List of networks to add
    """
    networks_list: Optional[List[SingleNetwork]] = None

    def __post_init__(self):
        super().__init__()

    def get_method(self) -> HttpMethod:
        return HttpMethod.POST

    def get_url(self) -> str:
        return RequestUrlCollection.BATCH_ADDING_NETWORKS


@dataclass
class BatchAddingNetworksResult:
    """Batch adding networks result data."""
    task_id: Optional[str] = None


class BatchAddingNetworksResponse(TAUCResponse[BatchAddingNetworksResult]):
    """Response for batch adding networks operation."""

    def _parse_result(self, result_data: dict) -> Optional[BatchAddingNetworksResult]:
        """Parse batch adding networks result."""
        if not result_data:
            return None

        return BatchAddingNetworksResult(
            task_id=result_data.get("taskId")
        )

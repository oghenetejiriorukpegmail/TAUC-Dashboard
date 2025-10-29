"""Get batch adding result request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection
from .add_network import PreConfig, Tag


@dataclass
class BatchMeshUnit:
    """Mesh unit information with error info."""
    sn: Optional[str] = None
    mac: Optional[str] = None
    error_info: Optional[str] = None


@dataclass
class GetBatchAddingResultRequest(TAUCRequest):
    """
    Request to get batch adding result.

    Attributes:
        taskId: Task ID (must use camelCase to match URL path variable)
    """
    taskId: Optional[str] = None

    def __init__(self, task_id: str):
        super().__init__()
        self.taskId = task_id  # Set camelCase attribute for path variable

    def get_method(self) -> HttpMethod:
        return HttpMethod.GET

    def get_url(self) -> str:
        return RequestUrlCollection.GET_BATCH_ADDING_RESULT


@dataclass
class BatchAddingResultNetwork:
    """Network result in batch adding operation."""
    network_name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    olt: Optional[str] = None
    address: Optional[str] = None
    subscribe_download: Optional[str] = None
    subscribe_upload: Optional[str] = None
    subscribe_date: Optional[str] = None
    user_network_profile_city: Optional[str] = None
    mesh_unit_list: Optional[List[BatchMeshUnit]] = None
    tags: Optional[List[Tag]] = None
    pre_config: Optional[PreConfig] = None


class GetBatchAddingResultResponse(TAUCResponse[List[BatchAddingResultNetwork]]):
    """Response for get batch adding result operation."""

    def _parse_result(self, result_data) -> Optional[List[BatchAddingResultNetwork]]:
        """Parse batch adding result."""
        if not result_data:
            return None

        if not isinstance(result_data, list):
            return None

        networks = []
        for network_data in result_data:
            mesh_units = []
            if network_data.get("meshUnitList"):
                for unit in network_data["meshUnitList"]:
                    mesh_units.append(BatchMeshUnit(
                        sn=unit.get("sn"),
                        mac=unit.get("mac"),
                        error_info=unit.get("errorInfo")
                    ))

            tags = []
            if network_data.get("tags"):
                for tag_data in network_data["tags"]:
                    tags.append(Tag(
                        name=tag_data.get("name"),
                        value=tag_data.get("value")
                    ))

            # Parse pre_config if present
            pre_config = None
            if network_data.get("preConfig"):
                # Note: Full parsing of preConfig would require importing
                # and parsing all nested structures. For now, we'll set it to None
                # and can expand this later if needed.
                pass

            networks.append(BatchAddingResultNetwork(
                network_name=network_data.get("networkName"),
                username=network_data.get("username"),
                phone_number=network_data.get("phoneNumber"),
                email=network_data.get("email"),
                olt=network_data.get("olt"),
                address=network_data.get("address"),
                subscribe_download=network_data.get("subscribeDownload"),
                subscribe_upload=network_data.get("subscribeUpload"),
                subscribe_date=network_data.get("subscribeDate"),
                user_network_profile_city=network_data.get("userNetworkProfileCity"),
                mesh_unit_list=mesh_units if mesh_units else None,
                tags=tags if tags else None,
                pre_config=pre_config
            ))

        return networks

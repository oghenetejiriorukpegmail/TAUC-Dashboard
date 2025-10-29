"""Get NAT locked inventory request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class GetNATLockedInventoryRequest(TAUCRequest):
    """
    Request to get NAT-locked (suspended) devices.

    Attributes:
        page: Page number (optional)
        pageSize: Page size (optional) - NOTE: camelCase to match API
    """
    page: Optional[str] = None
    pageSize: Optional[str] = None

    def __init__(self, page: Optional[str] = None, pageSize: Optional[str] = None):
        super().__init__()
        self.page = page
        self.pageSize = pageSize

    def get_method(self) -> HttpMethod:
        return HttpMethod.GET

    def get_url(self) -> str:
        return RequestUrlCollection.GET_NAT_LOCKED_INVENTORY


@dataclass
class MeshUnit:
    """Mesh unit data."""
    sn: Optional[str] = None
    mac: Optional[str] = None


@dataclass
class InventoryData:
    """Inventory data for a network."""
    network_name: Optional[str] = None
    mesh_unit_list: Optional[List[MeshUnit]] = None


@dataclass
class NATLockedInventoryResult:
    """NAT locked inventory result data."""
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    data: Optional[List[InventoryData]] = None


class GetNATLockedInventoryResponse(TAUCResponse[NATLockedInventoryResult]):
    """Response containing NAT-locked devices."""

    def _parse_result(self, result_data: dict) -> NATLockedInventoryResult:
        """Parse NAT locked inventory result."""
        if isinstance(result_data, dict):
            # Parse data list
            data_list = []
            if result_data.get("data"):
                for item in result_data["data"]:
                    mesh_units = []
                    if item.get("meshUnitList"):
                        for unit in item["meshUnitList"]:
                            mesh_units.append(MeshUnit(
                                sn=unit.get("sn"),
                                mac=unit.get("mac")
                            ))
                    data_list.append(InventoryData(
                        network_name=item.get("networkName"),
                        mesh_unit_list=mesh_units
                    ))

            return NATLockedInventoryResult(
                total=result_data.get("total"),
                page=result_data.get("page"),
                page_size=result_data.get("pageSize"),
                data=data_list
            )
        return result_data

"""Get all inventory request and response models."""

from dataclasses import dataclass
from typing import Optional
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection
from .get_nat_locked_inventory import InventoryData, NATLockedInventoryResult


@dataclass
class GetAllInventoryRequest(TAUCRequest):
    """
    Request to get all inventory devices.

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
        return RequestUrlCollection.GET_ALL_INVENTORY


# Reuse the same result structure as NAT locked inventory
class GetAllInventoryResponse(TAUCResponse[NATLockedInventoryResult]):
    """Response containing all inventory devices."""

    def _parse_result(self, result_data: dict) -> NATLockedInventoryResult:
        """Parse inventory result (same structure as NAT locked)."""
        # Import here to avoid circular dependency
        from .get_nat_locked_inventory import GetNATLockedInventoryResponse, MeshUnit

        if isinstance(result_data, dict):
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

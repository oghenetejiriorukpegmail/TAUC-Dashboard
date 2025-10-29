"""Get network details request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class GetNetworkDetailsRequest(TAUCRequest):
    """
    Request to get network details.

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
        return RequestUrlCollection.GET_NETWORK_DETAILS


@dataclass
class NetworkMeshUnit:
    """Mesh unit in network."""
    sn: Optional[str] = None
    mac: Optional[str] = None
    device_id: Optional[str] = None
    topo_role: Optional[str] = None


@dataclass
class NetworkTag:
    """Network tag."""
    name: Optional[str] = None
    value: Optional[str] = None


@dataclass
class Network:
    """Network information."""
    id: Optional[int] = None
    network_name: Optional[str] = None
    address: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    mesh_unit_list: Optional[List[NetworkMeshUnit]] = None
    tags: Optional[List[NetworkTag]] = None
    # Add other fields as needed


@dataclass
class NetworkDetailsResult:
    """Network details result data."""
    network: Optional[Network] = None
    pre_config_enable: Optional[bool] = None
    # Add pre_config field as needed


class GetNetworkDetailsResponse(TAUCResponse[NetworkDetailsResult]):
    """Response containing network details."""

    def _parse_result(self, result_data: dict) -> NetworkDetailsResult:
        """Parse network details result."""
        if isinstance(result_data, dict):
            network_data = result_data.get("network")
            network = None

            if network_data:
                mesh_units = []
                if network_data.get("meshUnitList"):
                    for unit in network_data["meshUnitList"]:
                        mesh_units.append(NetworkMeshUnit(
                            sn=unit.get("sn"),
                            mac=unit.get("mac"),
                            device_id=unit.get("deviceId"),
                            topo_role=unit.get("topoRole")
                        ))

                tags = []
                if network_data.get("tags"):
                    for tag in network_data["tags"]:
                        tags.append(NetworkTag(
                            name=tag.get("name"),
                            value=tag.get("value")
                        ))

                network = Network(
                    id=network_data.get("id"),
                    network_name=network_data.get("networkName"),
                    address=network_data.get("address"),
                    username=network_data.get("username"),
                    phone_number=network_data.get("phoneNumber"),
                    email=network_data.get("email"),
                    mesh_unit_list=mesh_units,
                    tags=tags
                )

            return NetworkDetailsResult(
                network=network,
                pre_config_enable=result_data.get("preConfigEnable")
            )
        return result_data

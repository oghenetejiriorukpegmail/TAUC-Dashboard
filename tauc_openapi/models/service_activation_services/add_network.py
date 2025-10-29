"""Add network request and response models."""

from dataclasses import dataclass, field
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class PreConfigSipAlg:
    """SIP ALG configuration."""
    enable: Optional[bool] = None


@dataclass
class PreConfigWireless:
    """Wireless pre-configuration."""
    ssid: Optional[str] = None
    password: Optional[str] = None
    ssid_6g: Optional[str] = None
    password_6g: Optional[str] = None
    enable_band_steering: Optional[bool] = None
    ssid_2g: Optional[str] = None
    password_2g: Optional[str] = None
    ssid_5g: Optional[str] = None
    password_5g: Optional[str] = None


@dataclass
class PreConfigSipUserInfo:
    """SIP user information."""
    phone_number: Optional[str] = None
    account: Optional[str] = None
    password: Optional[str] = None


@dataclass
class PreConfigInternet:
    """Internet pre-configuration."""
    type: Optional[str] = None
    ip: Optional[str] = None
    ipv6: Optional[str] = None
    mask: Optional[str] = None
    gateway: Optional[str] = None
    vlan_enable: Optional[bool] = None
    vlan_id: Optional[int] = None
    vlan_priority: Optional[int] = None
    mtu_size: Optional[int] = None
    xdsl_mode: Optional[str] = None
    vci: Optional[int] = None
    vpi: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    vpn_server: Optional[str] = None
    primary_dns: Optional[str] = None
    secondary_dns: Optional[str] = None


@dataclass
class PreConfig:
    """Network pre-configuration."""
    operation_mode: Optional[str] = None
    internet: Optional[PreConfigInternet] = None
    wireless: Optional[PreConfigWireless] = None
    sip_user_info: Optional[PreConfigSipUserInfo] = None
    sip_alg: Optional[PreConfigSipAlg] = None


@dataclass
class MeshUnit:
    """Mesh unit information."""
    sn: Optional[str] = None
    mac: Optional[str] = None


@dataclass
class Tag:
    """Network tag."""
    name: Optional[str] = None
    value: Optional[str] = None


@dataclass
class AddNetworkRequest(TAUCRequest):
    """
    Request to add a new network.

    Attributes:
        network_name: Network name
        username: Username
        phone_number: Phone number
        email: Email address
        olt: OLT identifier
        address: Physical address
        config_type: Configuration type
        country: Country
        region_group: Region group
        state_or_province: State or province
        city: City
        district_or_postal_code: District or postal code
        site: Site information
        house_number: House number
        subscribe_download: Download subscription
        subscribe_upload: Upload subscription
        subscribe_date: Subscription date
        user_network_profile_city: User network profile city
        mesh_unit_list: List of mesh units
        tags: List of tags
        pre_config: Pre-configuration settings
    """
    network_name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    olt: Optional[str] = None
    address: Optional[str] = None
    config_type: Optional[int] = None
    country: Optional[str] = None
    region_group: Optional[str] = None
    state_or_province: Optional[str] = None
    city: Optional[str] = None
    district_or_postal_code: Optional[str] = None
    site: Optional[str] = None
    house_number: Optional[str] = None
    subscribe_download: Optional[str] = None
    subscribe_upload: Optional[str] = None
    subscribe_date: Optional[str] = None
    user_network_profile_city: Optional[str] = None
    mesh_unit_list: Optional[List[MeshUnit]] = None
    tags: Optional[List[Tag]] = None
    pre_config: Optional[PreConfig] = None

    def __post_init__(self):
        super().__init__()

    def get_method(self) -> HttpMethod:
        return HttpMethod.POST

    def get_url(self) -> str:
        return RequestUrlCollection.ADD_NETWORK


@dataclass
class FailedMeshUnit:
    """Failed mesh unit information."""
    sn: Optional[str] = None
    mac: Optional[str] = None
    error: Optional[str] = None


@dataclass
class AddNetworkResult:
    """Add network result data."""
    id: Optional[int] = None
    failed_mesh_unit_list: Optional[List[FailedMeshUnit]] = None


class AddNetworkResponse(TAUCResponse[AddNetworkResult]):
    """Response for add network operation."""

    def _parse_result(self, result_data) -> Optional[AddNetworkResult]:
        """Parse add network result."""
        if not result_data:
            return None

        # Handle case where result_data is a string (error message)
        if isinstance(result_data, str):
            # API returned a string error message instead of structured data
            return None

        # Handle normal dict response
        if not isinstance(result_data, dict):
            return None

        failed_units = []
        if result_data.get("failedMeshUnitList"):
            for unit in result_data["failedMeshUnitList"]:
                failed_units.append(FailedMeshUnit(
                    sn=unit.get("sn"),
                    mac=unit.get("mac"),
                    error=unit.get("error")
                ))

        return AddNetworkResult(
            id=result_data.get("id"),
            failed_mesh_unit_list=failed_units if failed_units else None
        )

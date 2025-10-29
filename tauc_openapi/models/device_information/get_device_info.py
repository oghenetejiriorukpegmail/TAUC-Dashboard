"""Get device info request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class GetDeviceInfoRequest(TAUCRequest):
    """
    Request to get detailed device information by device ID.

    Attributes:
        deviceId: Device ID (must use camelCase to match URL path variable)
    """
    deviceId: Optional[str] = None

    def __init__(self, device_id: str):
        super().__init__()
        self.deviceId = device_id  # Set camelCase attribute for path variable

    def get_method(self) -> HttpMethod:
        return HttpMethod.GET

    def get_url(self) -> str:
        return RequestUrlCollection.GET_DEVICE_INFO


@dataclass
class DeviceInfo:
    """
    Device information data.

    Attributes:
        device_id: Device ID
        mac: Device MAC address
        sn: Device serial number
        device_model: Device model (optional)
        fw_version: Firmware version (optional)
        imei: IMEI number (optional)
        topo_role: Topology role - MASTER, SLAVE, or INACTIVE
        device_category: Device category - DECO or AGINET
    """
    device_id: str
    mac: str
    sn: str
    topo_role: str
    device_category: str
    device_model: Optional[str] = None
    fw_version: Optional[str] = None
    imei: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DeviceInfo':
        """Create DeviceInfo from API response dict."""
        return cls(
            device_id=data.get("deviceId"),
            mac=data.get("mac"),
            sn=data.get("sn"),
            device_model=data.get("deviceModel"),
            fw_version=data.get("fwVersion"),
            imei=data.get("imei"),
            topo_role=data.get("topoRole"),
            device_category=data.get("deviceCategory")
        )


class GetDeviceInfoResponse(TAUCResponse[List[DeviceInfo]]):
    """Response containing device information list."""

    def _parse_result(self, result_data) -> Optional[List[DeviceInfo]]:
        """Parse device info result."""
        if not result_data:
            return None

        # API returns an array of device info objects
        if isinstance(result_data, list):
            return [DeviceInfo.from_dict(item) for item in result_data]
        elif isinstance(result_data, dict):
            # Handle single object case
            return [DeviceInfo.from_dict(result_data)]

        return None

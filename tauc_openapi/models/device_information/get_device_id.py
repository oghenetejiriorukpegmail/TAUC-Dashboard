"""Get device ID request and response models."""

from dataclasses import dataclass
from typing import Optional
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class GetDeviceIdRequest(TAUCRequest):
    """
    Request to get device ID by SN or MAC address.

    Attributes:
        sn: Serial number (optional)
        mac: MAC address (optional)
    """
    sn: Optional[str] = None
    mac: Optional[str] = None

    def __init__(self, sn: Optional[str] = None, mac: Optional[str] = None):
        super().__init__()
        self.sn = sn
        self.mac = mac

    def get_method(self) -> HttpMethod:
        return HttpMethod.GET

    def get_url(self) -> str:
        return RequestUrlCollection.GET_DEVICE_ID


@dataclass
class DeviceIdResult:
    """Device ID result data."""
    device_id: Optional[str] = None


class GetDeviceIdResponse(TAUCResponse[DeviceIdResult]):
    """Response containing device ID."""

    def _parse_result(self, result_data: dict) -> DeviceIdResult:
        """Parse device ID result."""
        if isinstance(result_data, dict):
            return DeviceIdResult(device_id=result_data.get("deviceId"))
        return result_data

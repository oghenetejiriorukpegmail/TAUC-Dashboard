"""Get network name list V2 request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class GetNetworkNameListV2Request(TAUCRequest):
    """
    Request to get network name list (V2).

    Attributes:
        page: Page number (optional)
        pageSize: Page size (optional) - NOTE: camelCase to match API
        networkStatus: Network status filter (optional) - NOTE: camelCase
        sn: Serial number filter (optional)
        mac: MAC address filter (optional)
        wanMac: WAN MAC address filter (optional) - NOTE: camelCase
        publicIp: Public IP filter (optional) - NOTE: camelCase
    """
    page: Optional[str] = None
    pageSize: Optional[str] = None
    networkStatus: Optional[str] = None
    sn: Optional[str] = None
    mac: Optional[str] = None
    wanMac: Optional[str] = None
    publicIp: Optional[str] = None

    def __init__(
        self,
        page: Optional[str] = None,
        pageSize: Optional[str] = None,
        networkStatus: Optional[str] = None,
        sn: Optional[str] = None,
        mac: Optional[str] = None,
        wanMac: Optional[str] = None,
        publicIp: Optional[str] = None
    ):
        super().__init__()
        self.page = page
        self.pageSize = pageSize
        self.networkStatus = networkStatus
        self.sn = sn
        self.mac = mac
        self.wanMac = wanMac
        self.publicIp = publicIp

    def get_method(self) -> HttpMethod:
        return HttpMethod.GET

    def get_url(self) -> str:
        return RequestUrlCollection.GET_NETWORK_NAME_LIST_V2


@dataclass
class NetworkData:
    """Network data with ID and name."""
    id: Optional[int] = None
    network_name: Optional[str] = None


@dataclass
class GetNetworkNameListV2Result:
    """Get network name list V2 result data."""
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    data: Optional[List[NetworkData]] = None


class GetNetworkNameListV2Response(TAUCResponse[GetNetworkNameListV2Result]):
    """Response for get network name list V2 operation."""

    def _parse_result(self, result_data) -> Optional[GetNetworkNameListV2Result]:
        """Parse get network name list V2 result."""
        if not result_data:
            return None

        if not isinstance(result_data, dict):
            return None

        # Parse data list
        data_list = []
        if result_data.get("data"):
            for item in result_data["data"]:
                data_list.append(NetworkData(
                    id=item.get("id"),
                    network_name=item.get("networkName")
                ))

        return GetNetworkNameListV2Result(
            total=result_data.get("total"),
            page=result_data.get("page"),
            page_size=result_data.get("pageSize"),
            data=data_list if len(data_list) > 0 else None
        )

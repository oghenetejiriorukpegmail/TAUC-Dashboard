"""Add asset request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class AddAssetRequest(TAUCRequest):
    """
    Request to add a new asset.

    Attributes:
        sn: Serial number
        mac: MAC address
    """
    sn: Optional[str] = None
    mac: Optional[str] = None

    def __post_init__(self):
        super().__init__()

    def get_method(self) -> HttpMethod:
        return HttpMethod.POST

    def get_url(self) -> str:
        return RequestUrlCollection.ADD_ASSET


@dataclass
class FailedAsset:
    """Failed asset information."""
    error_code: Optional[int] = None
    message: Optional[str] = None
    sn: Optional[str] = None
    mac: Optional[str] = None


@dataclass
class AddAssetResult:
    """Add asset result data."""
    failed_assets: Optional[List[FailedAsset]] = None


class AddAssetResponse(TAUCResponse[AddAssetResult]):
    """Response for add asset operation."""

    def _parse_result(self, result_data: dict) -> Optional[AddAssetResult]:
        """Parse add asset result."""
        if not result_data:
            return None

        failed_assets = []
        if result_data.get("failedAssets"):
            for asset in result_data["failedAssets"]:
                failed_assets.append(FailedAsset(
                    error_code=asset.get("errorCode"),
                    message=asset.get("message"),
                    sn=asset.get("sn"),
                    mac=asset.get("mac")
                ))

        return AddAssetResult(
            failed_assets=failed_assets if failed_assets else None
        )

"""Delete asset request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class Asset:
    """Asset information for deletion."""
    sn: Optional[str] = None
    mac: Optional[str] = None


@dataclass
class DeleteAssetRequest(TAUCRequest):
    """
    Request to delete a device asset.

    Attributes:
        asset: Asset information (SN and MAC)
        deletion_type: Type of deletion operation
    """
    asset: Optional[Asset] = None
    deletion_type: Optional[int] = None

    def __post_init__(self):
        super().__init__()

    def get_method(self) -> HttpMethod:
        return HttpMethod.POST

    def get_url(self) -> str:
        return RequestUrlCollection.DELETE_ASSET


@dataclass
class FailedAsset:
    """Failed asset information."""
    error_code: Optional[int] = None
    message: Optional[str] = None
    sn: Optional[str] = None
    mac: Optional[str] = None


@dataclass
class DeleteAssetResult:
    """Delete asset result data."""
    failed_assets: Optional[List[FailedAsset]] = None


class DeleteAssetResponse(TAUCResponse[DeleteAssetResult]):
    """Response for delete asset operation."""

    def _parse_result(self, result_data) -> Optional[DeleteAssetResult]:
        """Parse delete asset result."""
        if not result_data:
            return None

        if not isinstance(result_data, dict):
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

        return DeleteAssetResult(
            failed_assets=failed_assets if failed_assets else None
        )

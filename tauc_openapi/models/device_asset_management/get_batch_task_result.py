"""Get batch task result request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection
from .add_asset import FailedAsset


@dataclass
class GetBatchTaskResultRequest(TAUCRequest):
    """
    Request to get batch task result.

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
        return RequestUrlCollection.GET_BATCH_TASK_RESULT


@dataclass
class GetBatchTaskResultData:
    """Batch task result data."""
    failed_assets: Optional[List[FailedAsset]] = None


class GetBatchTaskResultResponse(TAUCResponse[GetBatchTaskResultData]):
    """Response for get batch task result operation."""

    def _parse_result(self, result_data: dict) -> Optional[GetBatchTaskResultData]:
        """Parse batch task result."""
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

        return GetBatchTaskResultData(
            failed_assets=failed_assets if failed_assets else None
        )

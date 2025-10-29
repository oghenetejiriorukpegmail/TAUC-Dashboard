"""Batch add assets request and response models."""

from dataclasses import dataclass
from typing import Optional, List
from ...base.tauc_request import TAUCRequest, HttpMethod
from ...base.tauc_response import TAUCResponse
from ...base.request_url_collection import RequestUrlCollection


@dataclass
class Asset:
    """Asset information."""
    sn: Optional[str] = None
    mac: Optional[str] = None


@dataclass
class BatchAddingAssetsRequest(TAUCRequest):
    """
    Request to batch add multiple assets.

    Attributes:
        assets: List of assets to add
    """
    assets: Optional[List[Asset]] = None

    def __post_init__(self):
        super().__init__()

    def get_method(self) -> HttpMethod:
        return HttpMethod.POST

    def get_url(self) -> str:
        return RequestUrlCollection.BATCH_ADDING_ASSETS


@dataclass
class BatchAddingAssetsResult:
    """Batch adding assets result data."""
    task_id: Optional[str] = None
    new_task: Optional[bool] = None


class BatchAddingAssetsResponse(TAUCResponse[BatchAddingAssetsResult]):
    """Response for batch adding assets operation."""

    def _parse_result(self, result_data: dict) -> Optional[BatchAddingAssetsResult]:
        """Parse batch adding assets result."""
        if not result_data:
            return None

        return BatchAddingAssetsResult(
            task_id=result_data.get("taskId"),
            new_task=result_data.get("newTask")
        )

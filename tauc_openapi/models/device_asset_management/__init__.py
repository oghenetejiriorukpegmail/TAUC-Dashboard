"""Device asset management models."""

from .add_asset import (
    AddAssetRequest,
    AddAssetResponse,
    AddAssetResult,
    FailedAsset
)
from .batch_add_assets import (
    BatchAddingAssetsRequest,
    BatchAddingAssetsResponse,
    BatchAddingAssetsResult,
    Asset
)
from .get_batch_task_result import (
    GetBatchTaskResultRequest,
    GetBatchTaskResultResponse,
    GetBatchTaskResultData
)
from .delete_asset import (
    DeleteAssetRequest,
    DeleteAssetResponse,
    DeleteAssetResult
)

__all__ = [
    # Add Asset
    "AddAssetRequest",
    "AddAssetResponse",
    "AddAssetResult",
    "FailedAsset",

    # Batch Add Assets
    "BatchAddingAssetsRequest",
    "BatchAddingAssetsResponse",
    "BatchAddingAssetsResult",
    "Asset",

    # Get Batch Task Result
    "GetBatchTaskResultRequest",
    "GetBatchTaskResultResponse",
    "GetBatchTaskResultData",

    # Delete Asset
    "DeleteAssetRequest",
    "DeleteAssetResponse",
    "DeleteAssetResult",
]

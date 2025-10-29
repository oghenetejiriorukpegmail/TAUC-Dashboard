"""Model classes for TAUC API requests and responses."""

# Access Token
from .access_token.get_access_token import GetAccessTokenRequest, GetAccessTokenResponse

# Device Information
from .device_information.get_device_id import GetDeviceIdRequest, GetDeviceIdResponse
from .device_information.get_device_info import GetDeviceInfoRequest, GetDeviceInfoResponse

# Inventory Management
from .inventory_management.get_all_inventory import GetAllInventoryRequest, GetAllInventoryResponse
from .inventory_management.get_nat_locked_inventory import GetNATLockedInventoryRequest, GetNATLockedInventoryResponse

# Network System Management
from .network_system_management.nat_lock import NATLockMeshControllerRequest, NATLockMeshControllerResponse
from .network_system_management.nat_unlock import NATUnlockMeshControllerRequest, NATUnlockMeshControllerResponse
from .network_system_management.get_network_status import GetNetworkStatusRequest, GetNetworkStatusResponse
from .network_system_management.get_network_details import GetNetworkDetailsRequest, GetNetworkDetailsResponse
from .network_system_management.get_network_name_list_v2 import GetNetworkNameListV2Request, GetNetworkNameListV2Response
from .network_system_management.delete_network import DeleteNetworkRequest, DeleteNetworkResponse

# Service Activation Services
from .service_activation_services import (
    AddNetworkRequest, AddNetworkResponse,
    BatchAddingNetworksRequest, BatchAddingNetworksResponse,
    GetBatchAddingResultRequest, GetBatchAddingResultResponse,
    DeleteNetworkListRequest, DeleteNetworkListResponse
)

# Device Asset Management
from .device_asset_management import (
    AddAssetRequest, AddAssetResponse,
    BatchAddingAssetsRequest, BatchAddingAssetsResponse,
    GetBatchTaskResultRequest, GetBatchTaskResultResponse,
    DeleteAssetRequest, DeleteAssetResponse
)

__all__ = [
    # Access Token
    "GetAccessTokenRequest",
    "GetAccessTokenResponse",
    # Device Information
    "GetDeviceIdRequest",
    "GetDeviceIdResponse",
    "GetDeviceInfoRequest",
    "GetDeviceInfoResponse",
    # Inventory Management
    "GetAllInventoryRequest",
    "GetAllInventoryResponse",
    "GetNATLockedInventoryRequest",
    "GetNATLockedInventoryResponse",
    # Network System Management
    "NATLockMeshControllerRequest",
    "NATLockMeshControllerResponse",
    "NATUnlockMeshControllerRequest",
    "NATUnlockMeshControllerResponse",
    "GetNetworkStatusRequest",
    "GetNetworkStatusResponse",
    "GetNetworkDetailsRequest",
    "GetNetworkDetailsResponse",
    "GetNetworkNameListV2Request",
    "GetNetworkNameListV2Response",
    "DeleteNetworkRequest",
    "DeleteNetworkResponse",
    # Service Activation Services
    "AddNetworkRequest",
    "AddNetworkResponse",
    "BatchAddingNetworksRequest",
    "BatchAddingNetworksResponse",
    "GetBatchAddingResultRequest",
    "GetBatchAddingResultResponse",
    "DeleteNetworkListRequest",
    "DeleteNetworkListResponse",
    # Device Asset Management
    "AddAssetRequest",
    "AddAssetResponse",
    "BatchAddingAssetsRequest",
    "BatchAddingAssetsResponse",
    "GetBatchTaskResultRequest",
    "GetBatchTaskResultResponse",
    "DeleteAssetRequest",
    "DeleteAssetResponse",
]

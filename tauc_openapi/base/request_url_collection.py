"""Collection of all TAUC API endpoint URLs."""


class RequestUrlCollection:
    """
    Constants for all TAUC API endpoint URLs.

    All endpoints are under the /v1/openapi/ base path.
    """

    # Access Token
    GET_ACCESS_TOKEN = "/v1/openapi/token"

    # Device Information
    GET_DEVICE_ID = "/v1/openapi/device-information/device-id"
    GET_DEVICE_INFO = "/v1/openapi/device-information/device-info/{deviceId}"

    # Network System Management
    GET_NETWORK_NAME = "/v1/openapi/network-system-management/name"
    GET_NETWORK_ID = "/v1/openapi/network-system-management/id"
    GET_TAGGED_NETWORK_LIST = "/v1/openapi/network-system-management/tagged-network-list"
    GET_NETWORK_STATUS = "/v1/openapi/network-system-management/status/{networkId}"
    GET_USER_DEFINED_TAG = "/v1/openapi/network-system-management/tag"
    GET_NETWORK_DETAILS = "/v1/openapi/network-system-management/details/{networkId}"
    ADD_MESH_RE = "/v1/openapi/network-system-management/mesh-re/{networkId}"
    DELETE_MESH_RE = "/v1/openapi/network-system-management/mesh-re/{networkId}"
    DELETE_NETWORK = "/v1/openapi/network-system-management/network/{networkId}"
    UPDATE_NETWORK_NAME = "/v1/openapi/network-system-management/name/{networkId}"
    UPDATE_NETWORK = "/v1/openapi/network-system-management/network/{networkId}"
    GET_NETWORK_NAME_LIST = "/v1/openapi/network-system-management/network-name-list/{networkStatus}"
    GET_NETWORK_NAME_LIST_V2 = "/v1/openapi/network-system-management/network-name-list"
    NAT_LOCK_MESH_CONTROLLER = "/v1/openapi/network-system-management/block/{networkId}"
    NAT_UNLOCK_MESH_CONTROLLER = "/v1/openapi/network-system-management/unblock/{networkId}"
    GET_HOMESHIELD_SUBSCRIPTION_STATUS = "/v1/openapi/network-system-management/homeshield-status/{networkId}"
    SUBSCRIBE_HOMESHIELD = "/v1/openapi/network-system-management/homeshield-subscribe/{networkId}"
    UNSUBSCRIBE_HOMESHIELD = "/v1/openapi/network-system-management/homeshield-unsubscribe/{networkId}"
    HOMESHIELD_STATISTIC = "/v1/openapi/network-system-management/homeshield-statistic"
    GET_NETWORK_MAP_URL = "/v1/openapi/network-system-management/redirect-network-map"
    GET_NETWORK_INFO_BY_PPPOE_USERNAME = "/v1/openapi/network-system-management/network-info/pppoe-username"

    # Inventory Management
    GET_ALL_INVENTORY = "/v1/openapi/inventory-management/all-inventory"
    GET_INACTIVATIVED_INVENTORY = "/v1/openapi/inventory-management/inactive-inventory"
    GET_NAT_LOCKED_INVENTORY = "/v1/openapi/inventory-management/nat-locked-inventory"

    # Device Management - WiFi SSID
    GET_WIFI_SSID_DECO = "/v1/openapi/device-management/deco/wifi-ssid/{deviceId}"
    GET_WIFI_SSID_AGINET = "/v1/openapi/device-management/aginet/wifi-ssid/{deviceId}"
    GET_GUEST_WIFI_SSID_AGINET = "/v1/openapi/device-management/aginet/guest-wifi-ssid/{networkId}"
    MODIFY_WIFI_SSID_DECO = "/v1/openapi/device-management/deco/wifi-ssid/{deviceId}"
    MODIFY_WIFI_SSID_AGINET = "/v1/openapi/device-management/aginet/wifi-ssid/{deviceId}"
    MODIFY_GUEST_WIFI_SSID_AGINET = "/v1/openapi/device-management/aginet/guest-wifi-ssid/{networkId}"

    # Device Management - WiFi Password
    MODIFY_WIFI_PASSWORD_DECO = "/v1/openapi/device-management/deco/wifi-password/{deviceId}"
    GET_WIFI_PASSWORD_AGINET = "/v1/openapi/device-management/aginet/wifi-password/{deviceId}"
    MODIFY_WIFI_PASSWORD_AGINET = "/v1/openapi/device-management/aginet/wifi-password/{deviceId}"

    # Device Management - Channels
    GET_24GHZ_CHANNEL_DECO = "/v1/openapi/device-management/deco/2g-channel/{deviceId}"
    GET_24GHZ_CHANNEL_AGINET = "/v1/openapi/device-management/aginet/2g-channel/{deviceId}"
    GET_5GHZ_CHANNEL_DECO = "/v1/openapi/device-management/deco/5g-channel/{deviceId}"
    GET_5GHZ_CHANNEL_AGINET = "/v1/openapi/device-management/aginet/5g-channel/{deviceId}"
    GET_6GHZ_CHANNEL_AGINET = "/v1/openapi/device-management/aginet/6g-channel/{deviceId}"
    MODIFY_24GHZ_CHANNEL_DECO = "/v1/openapi/device-management/deco/2g-channel/{deviceId}"
    MODIFY_24GHZ_CHANNEL_AGINET = "/v1/openapi/device-management/aginet/2g-channel/{deviceId}"
    MODIFY_5GHZ_CHANNEL_DECO = "/v1/openapi/device-management/deco/5g-channel/{deviceId}"
    MODIFY_5GHZ_CHANNEL_AGINET = "/v1/openapi/device-management/aginet/5g-channel/{deviceId}"
    MODIFY_6GHZ_CHANNEL_AGINET = "/v1/openapi/device-management/aginet/6g-channel/{deviceId}"

    # Device Management - Security
    GET_SECURITY_DECO = "/v1/openapi/device-management/deco/security/{deviceId}"
    GET_SECURITY_AGINET = "/v1/openapi/device-management/aginet/security/{deviceId}"
    MODIFY_24GHZ_SECURITY_AGINET = "/v1/openapi/device-management/aginet/2g-security/{deviceId}"
    MODIFY_5GHZ_SECURITY_AGINET = "/v1/openapi/device-management/aginet/5g-security/{deviceId}"
    MODIFY_6GHZ_SECURITY_AGINET = "/v1/openapi/device-management/aginet/6g-security/{deviceId}"

    # Device Management - Reboot/Reset
    REBOOT_ALL_DECO = "/v1/openapi/device-management/deco/reboot-all/{deviceId}"
    REBOOT_ALL_AGINET = "/v1/openapi/device-management/aginet/reboot-all/{deviceId}"
    REBOOT_DEVICE_LIST_DECO = "/v1/openapi/device-management/deco/reboot/{deviceId}"
    REBOOT_DEVICE_LIST_AGINET = "/v1/openapi/device-management/aginet/reboot/{deviceId}"
    RESET_ALL_DECO = "/v1/openapi/device-management/deco/reset-all/{deviceId}"
    RESET_ALL_AGINET = "/v1/openapi/device-management/aginet/reset-all/{deviceId}"
    RESET_RE_DEVICE_LIST_DECO = "/v1/openapi/device-management/deco/reset-re/{deviceId}"
    RESET_RE_DEVICE_LIST_AGINET = "/v1/openapi/device-management/aginet/reset-re/{deviceId}"

    # Device Management - SIP/VoIP
    GET_SIP_ACCOUNT_AGINET = "/v1/openapi/device-management/aginet/sip-account/{networkId}"
    SET_SIP_ACCOUNT_AGINET = "/v1/openapi/device-management/aginet/sip-account/{networkId}"
    RESET_SIP_ACCOUNT_AGINET = "/v1/openapi/device-management/aginet/sip-account-reset/{networkId}"
    GET_SIP_ACCOUNT_DECO = "/v1/openapi/device-management/deco/telephony/sip-account/{deviceId}"
    SET_SIP_ACCOUNT_DECO = "/v1/openapi/device-management/deco/telephony/sip-account/{deviceId}"
    RESET_SIP_ACCOUNT_DECO = "/v1/openapi/device-management/deco/telephony/sip-account-reset/{deviceId}"
    GET_SIP_OPTIONS_AGINET = "/v1/openapi/device-management/aginet/sip-options/{deviceId}"
    SET_SIP_OPTIONS_AGINET = "/v1/openapi/device-management/aginet/sip-options/{deviceId}"
    ENABLE_SIP_OPTIONS_AGINET = "/v1/openapi/device-management/aginet/sip-options/enable/{deviceId}"
    GET_VOIP_INFO_DECO = "/v1/openapi/device-management/deco/telephony/voip/{deviceId}"
    SET_VOIP_INFO_DECO = "/v1/openapi/device-management/deco/telephony/voip/{deviceId}"
    SET_SIP_VOIP = "/v1/openapi/device-management/aginet/cpe-swapping-setting/sip-voip/{deviceId}"
    GET_SIP_VOIP = "/v1/openapi/device-management/aginet/cpe-swapping-setting/sip-voip/{deviceId}"

    # Device Management - DHCP
    GET_DHCP_SERVER_V4_RESERVATION_LIST_AGINET = "/v1/openapi/device-management/aginet/ip-reservation/{deviceId}"
    CREATE_DHCP_SERVER_V4_RESERVATION_ENTRY_AGINET = "/v1/openapi/device-management/aginet/ip-reservation/{deviceId}"
    DELETE_DHCP_SERVER_V4_RESERVATION_ENTRY_AGINET = "/v1/openapi/device-management/aginet/ip-reservation/{deviceId}"
    MODIFY_DHCP_SERVER_V4_RESERVATION_ENTRY_AGINET = "/v1/openapi/device-management/aginet/ip-reservation/{deviceId}"
    SET_DHCP = "/v1/openapi/device-management/aginet/cpe-swapping-setting/dhcp/{deviceId}"
    GET_DHCP = "/v1/openapi/device-management/aginet/cpe-swapping-setting/dhcp/{deviceId}"

    # Device Management - Port Forwarding
    GET_PORT_FORWARDING_LIST_AGINET = "/v1/openapi/device-management/aginet/port-forwarding-list/{deviceId}"
    CREATE_PORT_FORWARDING_ENTRY_AGINET = "/v1/openapi/device-management/aginet/port-forwarding-entry/{deviceId}"
    DELETE_PORT_FORWARDING_ENTRY_AGINET = "/v1/openapi/device-management/aginet/port-forwarding-entry/{deviceId}"
    MODIFY_PORT_FORWARDING_ENTRY_AGINET = "/v1/openapi/device-management/aginet/port-forwarding-entry/{deviceId}"
    MODIFY_PORT_FORWARDING_ENTRY_STATUS_AGINET = "/v1/openapi/device-management/aginet/port-forwarding-entry-status/{deviceId}"

    # Device Management - UPnP & DMZ
    GET_UPNP_LIST_AGINET = "/v1/openapi/device-management/aginet/upnp-list/{networkId}"
    UPNP_ENABLE_AGINET = "/v1/openapi/device-management/aginet/upnp/enable/{networkId}"
    GET_DMZ_HOST_AGINET = "/v1/openapi/device-management/aginet/dmz-host/{networkId}"
    SET_DMZ_HOST_AGINET = "/v1/openapi/device-management/aginet/dmz-host/{networkId}"
    DMZ_ENABLE_AGINET = "/v1/openapi/device-management/aginet/dmz/enable/{networkId}"

    # Device Management - Network Interfaces
    GET_ETHERNET_IFNAMEALIAS_LIST_AGINET = "/v1/openapi/device-management/aginet/ethernet-interface-list/{networkId}"
    GET_IP_INTERFACE_LIST_AGINET = "/v1/openapi/device-management/aginet/ip-interface-list/{networkId}"

    # Device Management - Firmware
    UPGRADE_DEVICE_FIRMWARE_AGINET = "/v1/openapi/device-management/aginet/firmware-update/{deviceId}"
    UPGRADE_DEVICE_FIRMWARE_RESULT_AGINET = "/v1/openapi/device-management/aginet/firmware-update"

    # Device Management - MLO & Remote Management
    GET_MLO_AP_AGINET = "/v1/openapi/device-management/aginet/mlo-ap/{deviceId}"
    MODIFY_MLO_AP_AGINET = "/v1/openapi/device-management/aginet/mlo-ap/{deviceId}"
    GET_REMOTE_MANAGEMENT_INFO_AGINET = "/v1/openapi/device-management/aginet/remote-management/{networkId}"
    SET_REMOTE_MANAGEMENT_INFO_AGINET = "/v1/openapi/device-management/aginet/remote-management/{networkId}"

    # Device Management - CPE Swapping
    SET_WIRELESS = "/v1/openapi/device-management/aginet/cpe-swapping-setting/wireless/{deviceId}"
    GET_WIRELESS = "/v1/openapi/device-management/aginet/cpe-swapping-setting/wireless/{deviceId}"
    SET_LAN = "/v1/openapi/device-management/aginet/cpe-swapping-setting/lan/{deviceId}"
    GET_LAN = "/v1/openapi/device-management/aginet/cpe-swapping-setting/lan/{deviceId}"

    # Device Management - PPPoE & WiFi Power
    GET_PRE_CONFIGURATION_STATUS = "/v1/openapi/device-management/aginet/preconfiguration-status/{networkId}"
    PROFILE_PROVISIONING = "/v1/openapi/device-management/aginet/service-provisioning/{networkId}"
    GET_PPPOE_CONFIGURED_STATUS_WITH_CREDENTIALS = "/v1/openapi/device-management/aginet/pppoe-credentials/configured-status/{networkId}"
    MODIFY_PPPOE_CREDENTIALS = "/v1/openapi/device-management/aginet/pppoe-credentials/{networkId}"
    GET_PPPOE_CREDENTIALS = "/v1/openapi/device-management/aginet/pppoe-credentials/{networkId}"
    MODIFY_NETWORK_TRANSMIT_POWER_AGINET = "/v1/openapi/device-management/aginet/wifi-transmit-power/{networkId}"
    GET_NETWORK_TRANSMIT_POWER_AGINET = "/v1/openapi/device-management/aginet/wifi-transmit-power/{networkId}"

    # Device Management - Client Block/Unblock
    UNBLOCK_CLIENT_AGINET = "/v1/openapi/device-management/aginet/{networkId}/client/tr/unblock"
    BLOCK_CLIENT_AGINET = "/v1/openapi/device-management/aginet/{networkId}/client/tr/block"

    # Network Data Collection
    GET_WAN_INFO = "/v1/openapi/network-data-collection/wan-info/{deviceId}"
    GET_NETWORK_CLIENTS = "/v1/openapi/network-data-collection/network-clients/{networkId}"
    GET_MESH_TOPOLOGY_DATA = "/v1/openapi/network-data-collection/mesh-topology-data/{networkId}"
    GET_DECO_NETWORK_CLIENTS = "/v1/openapi/network-data-collection/network-clients/deco/{deviceId}"
    GET_NETWORK_CLIENTS_WITH_MLO = "/v1/openapi/network-data-collection/network-clients/{networkId}/mlo"
    GET_DECO_NETWORK_CLIENTS_V2 = "/v1/openapi/network-data-collection/network-clients/deco/v2/{deviceId}"
    GET_NETWORK_DEVICES_INFO = "/v1/openapi/network-data-collection/network-devices-info/{networkId}"

    # Network Topology Data Collection
    GET_ALL_CLIENT_ALERT_COUNT = "/v1/openapi/network-topology-data-collection/aginet/client-alert-count/{networkId}"
    GET_ALL_CLIENT_WIFI_METRICS = "/v1/openapi/network-topology-data-collection/aginet/client-wifi-metrics/{networkId}"
    GET_ALL_MESH_NODE_ALERT_COUNT = "/v1/openapi/network-topology-data-collection/aginet/mesh-node-alert-count/{networkId}"
    GET_ALL_MESH_NODE_HEALTH_CHECK = "/v1/openapi/network-topology-data-collection/aginet/mesh-node-health-check/{networkId}"
    GET_ALL_MESH_NODE_WIFI_METRICS = "/v1/openapi/network-topology-data-collection/aginet/mesh-node-wifi-metrics/{networkId}"
    GET_ALL_WIFI_CLIENT_HEALTH_CHECK = "/v1/openapi/network-topology-data-collection/aginet/client-health-check/{networkId}"

    # WiFi Management Data Collection
    GET_ALL_CLIENT_WIFI_KPI_METRICS = "/v1/openapi/wifi-manage-data-collection/aginet/client-wifi-kpi-metrics/{networkId}"
    GET_ALL_MESH_NODE_WIFI_KPI_METRICS = "/v1/openapi/wifi-manage-data-collection/aginet/mesh-node-wifi-kpi-metrics/{networkId}"
    GET_ALL_WIFI_ALERTS = "/v1/openapi/wifi-manage-data-collection/aginet/alert-info/{networkId}"
    GET_WIFI_METRIC_COLLECT_CONFIG = "/v1/openapi/wifi-manage-data-collection/aginet/wifi-metric-collect-config"
    GET_ALL_MESH_NODE_NETWORK_HEALTH_SCORE = "/v1/openapi/wifi-manage-data-collection/aginet/network-health-score/{networkId}"

    # Diagnostics
    DIAGNOSTICS = "/v1/openapi/diagnostics/{deviceId}"
    DIAGNOSTICS_RESULT = "/v1/openapi/diagnostics/result/{deviceId}"
    GET_KEY_PARAMETER_PERIOD_LOG = "/v1/openapi/diagnostics/kp-logs/{networkId}"

    # Container Application License (HomeShield/Sense)
    ENABLE_SENSE = "/v1/openapi/container-application-license/aginet/sense/enable/{networkId}"
    SET_SENSE_LICENSE_KEY = "/v1/openapi/container-application-license/aginet/sense-license-key/{networkId}"
    RESET_SENSE_LICENSE_KEY = "/v1/openapi/container-application-license/aginet/sense-reset-key/{networkId}"
    GET_SENSE_ACTIVATION_STATUS = "/v1/openapi/container-application-license/aginet/sense-activation-status/{networkId}"
    GET_SENSE_LICENSE_STATUS = "/v1/openapi/container-application-license/aginet/sense-license-status/{networkId}"
    TERMINATE_SENSE_LICENSE_KEY = "/v1/openapi/container-application-license/aginet/terminate-sense-license-key/{networkId}"
    LIST_ALL_CONTAINER_PROFILES = "/v1/openapi/container-application-license/aginet/container-profile-list"
    INSTALL_CONTAINER_DU = "/v1/openapi/container-application-license/aginet/control/du/{networkId}"
    UNINSTALL_SENSE_DU = "/v1/openapi/container-application-license/aginet/sense/uninstall/{networkId}"
    TERMINATE_SENSE_SERVICE = "/v1/openapi/container-application-license/aginet/terminate-sense-service/{networkId}"

    # RMA (Return Merchandise Authorization)
    RESTORE_CFG_AGINET = "/v1/openapi/rma/restore-cfg"
    RESTORE_RESULT_AGINET = "/v1/openapi/rma/restore-result"
    BACKUP_CFG_AGINET = "/v1/openapi/rma/backup-cfg"

    # TR-181 Data Model
    GET_EXTENSION_SET = "/v1/openapi/tr181-data-model-data-collection/aginet/{deviceId}/{uriPath}"
    SET_EXTENSION_SET = "/v1/openapi/tr181-data-model-data-collection/aginet/{deviceId}/{uriPath}"
    DELETE_EXTENSION_SET = "/v1/openapi/tr181-data-model-data-collection/aginet/{deviceId}/{path}"

    # Service Activation Services
    ADD_NETWORK = "/v1/openapi/service-activation-services/network"
    BATCH_ADDING_NETWORKS = "/v1/openapi/service-activation-services/networks"
    GET_BATCH_ADDING_RESULT = "/v1/openapi/service-activation-services/networks-result/{taskId}"
    DELETE_NETWORK_LIST = "/v1/openapi/service-activation-services/network-list"
    ESTABLISH_NETWORK = "/v1/openapi/service-activation-services/establish/network"
    GET_ESTABLISH_NETWORK_RESULT = "/v1/openapi/service-activation-services/establish/network"

    # Device Asset Management
    ADD_ASSET = "/v1/openapi/device-asset-management/device"
    BATCH_ADDING_ASSETS = "/v1/openapi/device-asset-management/devices"
    BATCH_DELETING_ASSETS = "/v1/openapi/device-asset-management/devices/delete"
    DELETE_ASSET = "/v1/openapi/device-asset-management/device/delete"
    GET_BATCH_TASK_RESULT = "/v1/openapi/device-asset-management/devices/devices-result/{taskId}"
    RESTORE_ASSET_FROM_RECYCLE_BIN = "/v1/openapi/device-asset-management/device/restore"

    # Network Health Monthly Reports
    GET_OVERALL_NETWORK_PERFORMANCE_MONTHLY_REPORT = "/v1/openapi/network-health-monthly-report/aginet/overall-network-performance/{networkId}"
    GET_AUTO_FINE_TUNING_MONTHLY_REPORT = "/v1/openapi/network-health-monthly-report/aginet/auto-fine-tuning/{networkId}"
    GET_INTERNET_SPEED_MONTHLY_REPORT = "/v1/openapi/network-health-monthly-report/aginet/internet-speed/{networkId}"
    GET_BROADBAND_USAGE_MONTHLY_REPORT = "/v1/openapi/network-health-monthly-report/aginet/broadband-usage/{networkId}"
    GET_INTERNET_QUALITY_MONTHLY_REPORT = "/v1/openapi/network-health-monthly-report/aginet/internet-quality/{networkId}"
    GET_WIFI_INTERFERENCE_MONTHLY_REPORT = "/v1/openapi/network-health-monthly-report/aginet/wifi-interference/{networkId}"
    GET_WIFI_COVERAGE_MONTHLY_REPORT = "/v1/openapi/network-health-monthly-report/aginet/wifi-coverage/{networkId}"
    GET_TRAFFIC_USAGE_MONTHLY_REPORT = "/v1/openapi/network-health-monthly-report/aginet/traffic-usage/{networkId}"

    # Profile Management
    LIST_ALL_TR_PARAMETER_PROFILES = "/v1/openapi/profile-management/aginet/tr-parameter-profiles"

    # Geomap Location Conversion
    BATCH_CONVERTING_ADDRESS = "/v1/openapi/geomap-location-conversion/networks"
    GET_BATCH_CONVERTING_RESULT = "/v1/openapi/geomap-location-conversion/result/{taskId}"

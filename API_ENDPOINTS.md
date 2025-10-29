# API Endpoints Used in Dashboard

This document lists all TAUC OpenAPI endpoints used in the Streamlit dashboard application.

## Base URL
```
https://use1-tauc-openapi.tplinkcloud.com
```

## Authentication Endpoints

### 1. Get Access Token (OAuth 2.0)
- **Endpoint:** `POST /v1/openapi/token`
- **Description:** Obtain OAuth 2.0 access token using client credentials
- **Used In:** Configuration page
- **Authentication:** Client certificate (mTLS), no X-Authorization signature required
- **Request:**
  ```
  client_id: string
  client_secret: string
  ```
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": {
      "access_token": "string",
      "expires_in": 86400,
      "token_type": "Bearer"
    }
  }
  ```

## Inventory Management Endpoints

### 2. Get All Inventory
- **Endpoint:** `GET /v1/openapi/inventory-management/all-inventory`
- **Description:** Get all the networks of inventory type under the account, including NAT blocked and inactive network
- **Used In:** Inventory page → "All Inventory" tab
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Query Parameters:**
  - `page`: Page number (string). **NOTE: 0 is the first page** (zero-indexed)
  - `pageSize`: Number of items per page (string). Positive integer, maximum value: 100
- **Example:** `GET /v1/openapi/inventory-management/all-inventory?page=0&pageSize=10`
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": {
      "total": 2,
      "page": 0,
      "pageSize": 10,
      "data": [
        {
          "networkName": "customer_1",
          "meshUnitList": [
            {
              "sn": "2252AMJ000011_2025/06/28_18:39",
              "mac": "3C-6A-D2-56-32-E8"
            }
          ]
        }
      ]
    }
  }
  ```

**Note:** The dashboard automatically handles page numbering, converting from 1-based (UI) to 0-based (API).

### 3. Get NAT-Locked Inventory
- **Endpoint:** `GET /v1/openapi/inventory-management/nat-locked-inventory`
- **Description:** Retrieve devices that have been NAT-locked (suspended)
- **Used In:** Inventory page → "NAT-Locked Devices" tab
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Query Parameters:**
  - `page`: Page number (string)
  - `pageSize`: Number of items per page (string)
- **Example:** `GET /v1/openapi/inventory-management/nat-locked-inventory?page=1&pageSize=10`
- **Response:** Same structure as Get All Inventory

## Network System Management Endpoints

### 4. Get Network ID by Name
- **Endpoint:** `GET /v1/openapi/network-system-management/id`
- **Description:** Look up network ID using network name
- **Used In:** All Network Management operations (automatic lookup)
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Query Parameters:**
  - `networkName`: Network name to look up (string)
- **Example:** `GET /v1/openapi/network-system-management/id?networkName=customer_1`
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": [
      {
        "networkName": "customer_1",
        "id": 12345
      }
    ]
  }
  ```

### 5. Lock NAT (Block Network)
- **Endpoint:** `POST /v1/openapi/network-system-management/block/{networkId}`
- **Description:** Suspend a network by locking NAT functionality
- **Used In:** Network Management page → "NAT Control" tab
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Path Parameters:**
  - `networkId`: Network ID (numeric)
- **Example:** `POST /v1/openapi/network-system-management/block/12345`
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": null
  }
  ```

### 6. Unlock NAT (Unblock Network)
- **Endpoint:** `POST /v1/openapi/network-system-management/unblock/{networkId}`
- **Description:** Resume a suspended network by unlocking NAT
- **Used In:** Network Management page → "NAT Control" tab
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Path Parameters:**
  - `networkId`: Network ID (numeric)
- **Example:** `POST /v1/openapi/network-system-management/unblock/12345`
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": null
  }
  ```

### 7. Get Network Status
- **Endpoint:** `GET /v1/openapi/network-system-management/status/{networkId}`
- **Description:** Get current status of a network
- **Used In:** Network Management page → "Network Status" tab
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Path Parameters:**
  - `networkId`: Network ID (numeric)
- **Example:** `GET /v1/openapi/network-system-management/status/12345`
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": {
      "status": "active",
      "networkId": 12345,
      "networkName": "customer_1"
    }
  }
  ```

### 8. Get Network Details
- **Endpoint:** `GET /v1/openapi/network-system-management/details/{networkId}`
- **Description:** Get comprehensive details about a network including all devices
- **Used In:** Network Management page → "Network Details" tab
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Path Parameters:**
  - `networkId`: Network ID (numeric)
- **Example:** `GET /v1/openapi/network-system-management/details/12345`
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": {
      "network": {
        "networkId": 12345,
        "networkName": "customer_1",
        "address": "123 Main St",
        "createTime": "2023-01-01T00:00:00Z",
        "meshUnitList": [
          {
            "sn": "serial123",
            "mac": "AA:BB:CC:DD:EE:FF",
            "topoRole": "MASTER",
            "model": "Deco X50"
          }
        ]
      }
    }
  }
  ```

## Device Information Endpoints

### 9. Get Device ID
- **Endpoint:** `GET /v1/openapi/device-information/device-id`
- **Description:** Look up device ID using MAC address AND serial number
- **Used In:** Device Lookup page
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Query Parameters:**
  - `sn`: Serial number (string, **required**) - 13 or 18 characters
  - `mac`: MAC address (string, **required**) - 12 characters, no separators
  - **Note:** **Both** `sn` AND `mac` are required together
- **Example:**
  - `GET /v1/openapi/device-information/device-id?sn=22360N3001039&mac=40E00CE190E`
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": {
      "deviceId": "ps305BtiEcom_AAA_lwu6cnhNc_YjQWbqvpfIsxH8cV-W1-xOoM7dyWn88888888"
    }
  }
  ```

### 10. Get Device Info
- **Endpoint:** `GET /v1/openapi/device-information/device-info/{deviceId}`
- **Description:** Get detailed device information including model, firmware, and topology role
- **Used In:** Device Lookup page (automatically called after getting device ID)
- **Authentication:** OAuth Bearer token + X-Authorization signature
- **Path Parameters:**
  - `deviceId`: Device ID obtained from Get Device ID endpoint
- **Example:**
  - `GET /v1/openapi/device-information/device-info/ps305BtiEcom_AAA_lwu6cnhNc_YjQWbqvpfIsxH8cV-W1-xOoM7dyWn88888888`
- **Response:**
  ```json
  {
    "errorCode": 0,
    "msg": "ok",
    "result": [
      {
        "deviceId": "ps305BtiEcom_AAA_lwu6cnhNc_YjQWbqvpfIsxH8cV-W1-xOoM7dyWn88888888",
        "mac": "40E00CE190E",
        "sn": "22360N3001039",
        "deviceModel": "Deco X50",
        "fwVersion": "1.2.5 Build 20231120 Rel. 55057",
        "imei": null,
        "topoRole": "MASTER",
        "deviceCategory": "DECO"
      }
    ]
  }
  ```
- **Topology Roles:**
  - `MASTER`: The main device (FAP) of the network - primary router/gateway
  - `SLAVE`: A satellite device extending network coverage (mesh node/repeater)
  - `INACTIVE`: The device hasn't been activated yet
- **Device Categories:**
  - `DECO`: TP-Link Deco mesh system devices
  - `AGINET`: TP-Link Aginet router/gateway devices

## Authentication Details

### X-Authorization Signature
All authenticated endpoints (except token acquisition) require:

1. **Authorization Header:**
   ```
   Authorization: Bearer {access_token}
   ```

2. **X-Authorization Header:**
   ```
   X-Authorization: Nonce={uuid},Signature={hmac_sha256_hex},Timestamp={unix_seconds}
   ```

3. **Signature Algorithm:**
   ```
   String-to-sign = [Content-MD5 + "\n"] + Timestamp + "\n" + Nonce + "\n" + URL_Path
   Signature = HMAC-SHA256(client_secret, string-to-sign)
   ```

## Error Codes

Common error codes you may encounter:

| Code | Message | Description |
|------|---------|-------------|
| 0 | ok | Success |
| -70301 | Network does not exist | Network name not found |
| -70325 | failed to validate params | Invalid parameters |
| -70411 | X-Authorization header info is empty | Missing signature |
| -70413 | X-Authorization wrong format | Invalid signature format |
| -70435 | Invalid token | Token expired or invalid |
| -40310 | No data found | Resource exists but no data |

## Endpoint Summary by Page

### Configuration Page
- `POST /v1/openapi/token` - Get access token

### Inventory Page
- `GET /v1/openapi/inventory-management/all-inventory` - All devices
- `GET /v1/openapi/inventory-management/nat-locked-inventory` - NAT-locked devices

### Network Management Page
- `GET /v1/openapi/network-system-management/id` - Lookup network ID
- `POST /v1/openapi/network-system-management/block/{networkId}` - Lock NAT
- `POST /v1/openapi/network-system-management/unblock/{networkId}` - Unlock NAT
- `GET /v1/openapi/network-system-management/status/{networkId}` - Get status
- `GET /v1/openapi/network-system-management/details/{networkId}` - Get details

### Device Lookup Page
- `GET /v1/openapi/device-information/device-id` - Get device ID by SN and MAC
- `GET /v1/openapi/device-information/device-info/{deviceId}` - Get detailed device information

## Total Endpoints Used
**10 unique endpoints** are implemented in this dashboard

## Viewing Endpoints in the UI

The dashboard now displays the endpoint being called:
- **Before API call:** Shows the endpoint in a code block (📡 icon)
- **In JSON response viewer:** Shows the endpoint used for that call
- **Format:** Method and full path with parameters

Example display:
```
📡 Endpoint: GET /v1/openapi/inventory-management/all-inventory?page=1&pageSize=10
```

This helps with:
- **Debugging:** See exactly which endpoint was called
- **Learning:** Understand the API structure
- **Documentation:** Know which endpoints to use in your own code
- **Troubleshooting:** Identify issues with specific endpoints

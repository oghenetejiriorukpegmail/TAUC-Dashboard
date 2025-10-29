# Device Lookup Fix: Both Parameters Required

**Date:** 2025-10-24
**Issue:** Device lookup failing with error -70346 "Invalid Parameter"
**Status:** ✅ FIXED

---

## Problem Description

Device lookup was failing with error:
```
Device not found: The parameter is invalid, please check the parameter. (Code: -70346)
```

Users were trying to search for devices using either:
- Serial Number alone
- MAC Address alone

But the API was rejecting both approaches.

---

## Root Cause Analysis

### The Incorrect Assumption

The dashboard UI allowed users to search by **either** SN **or** MAC:
```python
# WRONG - Dashboard offered two options
lookup_method = st.radio(
    "Lookup Method",
    ["By MAC Address", "By Serial Number"],
    horizontal=True
)

# WRONG - Only sending one parameter
if mac:
    request = GetDeviceIdRequest(mac=mac)
else:
    request = GetDeviceIdRequest(sn=sn)
```

### The API Reality

From official TAUC API documentation:

```
Query Parameters:
Name    Required    Description
sn      Yes         Device SN (13 or 18 characters)
mac     Yes         Device MAC (12 characters, no separators)
```

**Both parameters are REQUIRED together, not optional alternatives.**

### Why This Was Confusing

1. **Python SDK Model** - Both fields were `Optional`:
   ```python
   class GetDeviceIdRequest(TAUCRequest):
       sn: Optional[str] = None
       mac: Optional[str] = None
   ```

2. **Java SDK Model** - No `@NotNull` annotations:
   ```java
   @TAUCRequestQuery
   public String sn;

   @TAUCRequestQuery
   public String mac;
   ```

Both SDKs made the fields technically optional in code, but the **API requires both**.

---

## Solution

### Updated Dashboard UI

**Before:**
- Radio button: "By MAC Address" OR "By Serial Number"
- One input field at a time

**After:**
- Both fields displayed together
- Clear message: "Both Serial Number AND MAC Address are required"
- Validation for both fields

```python
def lookup_device():
    """Lookup device by SN and MAC (both required)."""
    st.info("""
    **Both Serial Number AND MAC Address are required.**

    You can find both values in:
    - Network Management → Network Details → Devices table
    - Inventory → Device list
    """)

    col1, col2 = st.columns(2)

    with col1:
        serial_number = st.text_input(
            "Serial Number (SN)",
            placeholder="22360N3001039",
            help="Device serial number (13 or 18 characters)"
        )

    with col2:
        mac_address = st.text_input(
            "MAC Address",
            placeholder="40E00CE190E or 40:E0:0C:E1:90:E",
            help="Device MAC address (12 characters)"
        )
```

### Updated Request Function

**Before:**
```python
def search_device(mac: str = None, sn: str = None):
    # Only one parameter sent
    if mac:
        request = GetDeviceIdRequest(mac=mac)
    else:
        request = GetDeviceIdRequest(sn=sn)
```

**After:**
```python
def search_device(sn: str, mac: str):
    """Search for device by SN and MAC (both required)."""
    # Both parameters always sent
    request = GetDeviceIdRequest(sn=sn, mac=mac)
```

### MAC Address Cleaning

Added automatic formatting:
```python
# Clean MAC address - remove separators
clean_mac = mac_address.replace(":", "").replace("-", "").upper()

# API expects: 40E00CE190E (no separators)
# Users can enter: 40:E0:0C:E1:90:E or 40-E0-0C-E1-90-E
```

---

## API Requirements

### Serial Number Format
- **Length:** 13 or 18 characters
- **Characters:** Uppercase letters, lowercase letters, numbers
- **Example:** `22360N3001039` (13 chars)

### MAC Address Format
- **Length:** Exactly 12 characters
- **Characters:** Letters A-F (uppercase/lowercase) and numbers
- **Format:** No separators (colons, hyphens, or dots)
- **Example:** `40E00CE190E`
- **Not accepted:** `40:E0:0C:E1:90:E` (dashboard removes separators automatically)

---

## How to Use Device Lookup Now

### Step 1: Get Device Information

Go to **Network Management → Network Details**:
1. Enter network name (e.g., "orukpe_home")
2. Click "Get Details"
3. Find the device in the "Devices in Network" table

You'll see:
- **Serial Number:** `22360N3001039`
- **MAC Address:** `40E00CE190E`
- **Device ID:** `TCDfTusKvvS5wER90gx3EgqE...`
- **Topo Role:** `MASTER`

### Step 2: Look Up Device ID

Go to **Device Lookup**:
1. Enter **Serial Number:** `22360N3001039`
2. Enter **MAC Address:** `40E00CE190E` (or with separators like `40:E0:0C:E1:90:E`)
3. Click "Search Device"

### Step 3: Get Device ID

Success response:
```json
{
  "errorCode": 0,
  "msg": "ok",
  "result": {
    "deviceId": "ps305BtiEcom_AAA_lwu6cnhNc_YjQWbqvpfIsxH8cV-W1-xOoM7dyWn88888888"
  }
}
```

---

## Testing

### Test Case: Valid Device Lookup

**Inputs:**
- SN: `22360N3001039`
- MAC: `40E00CE190E`

**Expected Result:**
```
✓ Device found!
Device ID: ps305BtiEcom_AAA_...
```

### Test Case: Missing Parameter

**Inputs:**
- SN: `22360N3001039`
- MAC: *(empty)*

**Expected Result:**
```
⚠️ Both Serial Number AND MAC Address are required!
```

### Test Case: MAC with Separators

**Inputs:**
- SN: `22360N3001039`
- MAC: `40:E0:0C:E1:90:E` (with colons)

**Expected Result:**
- Dashboard automatically cleans to: `40E00CE190E`
- Lookup succeeds

---

## Files Modified

### Dashboard
1. **`/streamlit_app/pages/device_lookup.py`**
   - Removed radio button selection (by MAC OR by SN)
   - Added combined input form (SN AND MAC)
   - Updated `search_device()` to require both parameters
   - Added MAC address cleaning/normalization
   - Added validation for field lengths

### Documentation
2. **`/streamlit_app/API_ENDPOINTS.md`**
   - Updated endpoint documentation
   - Marked both `sn` and `mac` as **required**
   - Updated example to show both parameters
   - Clarified parameter formats

---

## Why This Matters

**Device ID** is used for many other API operations:
- Get WiFi SSID
- Get device channels (2.4GHz, 5GHz, 6GHz)
- Reboot device
- Update firmware
- And many more device-specific operations

Without the correct Device ID, these operations cannot be performed. The lookup must work correctly to enable all device management features.

---

## API Compliance

The dashboard now correctly implements the TAUC API specification:

**Official API Docs:**
```
GET /v1/openapi/device-information/device-id

Query Parameters:
  sn (required): Device SN
  mac (required): Device MAC

Response:
  result.deviceId: Encrypted device identifier
```

**Dashboard Implementation:**
✅ Requests both SN and MAC from user
✅ Validates both fields are provided
✅ Cleans MAC address format automatically
✅ Sends both parameters together in request
✅ Displays encrypted Device ID from response

---

## Conclusion

This was a **critical misunderstanding** of the API requirements. The endpoint name "Get Device ID" and the SDK models suggested flexibility in parameter choice, but the API strictly requires **both** SN and MAC together.

**Key Lesson:** Always verify API requirements in official documentation, not just SDK signatures. Optional types in code don't always mean optional in the API contract.

The Device Lookup feature now works correctly and matches the official TAUC API specification!

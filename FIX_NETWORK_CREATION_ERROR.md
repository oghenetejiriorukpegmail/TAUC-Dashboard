# Fix for Network Creation Error -70325

## Problem

When attempting to create a network via the "Service Activation" page, the API returned error:
```
Failed to create network: failed to validate params (Code: -70325)
```

## Root Cause

The Python SDK was sending JSON with **snake_case** field names, but the TAUC API expects **camelCase** field names (matching the Java SDK).

### Example of the Issue:

**Python SDK was sending:**
```json
{
  "network_name": "TpJinkeworld",
  "mesh_unit_list": [
    {
      "sn": "2248H7N0G0Z",
      "mac": "2C:AE:CF:AB:8C:C5"
    }
  ],
  "pre_config": {
    "operation_mode": "Router",
    "wireless": {
      "ssid": "MyNetwork",
      "password": "password123",
      "enable_band_steering": true
    }
  }
}
```

**API expected (camelCase):**
```json
{
  "networkName": "TpJinkeworld",
  "meshUnitList": [
    {
      "sn": "2248H7N0G0Z",
      "mac": "2C:AE:CF:AB:8C:C5"
    }
  ],
  "preConfig": {
    "operationMode": "Router",
    "wireless": {
      "ssid": "MyNetwork",
      "password": "password123",
      "enableBandSteering": true
    }
  }
}
```

## Solution

Modified `/home/oghenetejiri/apps/TAUC-Dashboard/tauc_openapi/base/request_utils.py`:

1. **Added `_to_camel_case_dict()` method** - Recursively converts dictionary keys from snake_case to camelCase, filtering out `null` values
2. **Updated `_json_serializer()` method** - Now converts dataclass fields to camelCase when serializing
3. **Updated `process_request_body()` method** - Converts the main request body to camelCase before JSON serialization

### Key Features of the Fix:

- **Recursive conversion**: Handles nested objects and lists
- **Null filtering**: Omits fields with `None` values (matching Java SDK behavior)
- **Clean JSON**: Only sends fields with actual values

### Code Changes:

```python
@staticmethod
def _to_camel_case_dict(snake_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Convert dictionary with snake_case keys to camelCase keys."""
    camel_dict = {}
    for key, value in snake_dict.items():
        # Convert key to camelCase
        camel_key = RequestUtils._to_camel_case(key)

        # Recursively convert nested dictionaries
        if isinstance(value, dict):
            camel_dict[camel_key] = RequestUtils._to_camel_case_dict(value)
        elif isinstance(value, list):
            camel_dict[camel_key] = [
                RequestUtils._to_camel_case_dict(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            camel_dict[camel_key] = value

    return camel_dict
```

## Testing

After applying this fix, network creation should work properly. The API will now receive field names in the expected camelCase format.

## Impact

This fix affects **all API requests** that send JSON bodies, ensuring they match the Java SDK convention and API expectations. This includes:

- Add Network
- Batch Add Networks
- Add Device Asset
- Any other operations that send complex JSON payloads

## Next Steps

1. Restart the Streamlit app to load the updated code
2. Try creating the network again
3. Verify that the error no longer occurs

## Files Modified

- `tauc_openapi/base/request_utils.py` - Added camelCase conversion logic

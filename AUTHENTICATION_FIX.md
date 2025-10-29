# Authentication Fix - Error Code -70411

## Problem

When attempting to authenticate with the TAUC API, users encountered the error:
```
Error: X-Authorization header info is empty (Code: -70411)
```

## Root Causes

Three issues were identified and fixed:

### 1. Wrong OAuth Header Name
**Issue:** The SDK was sending `Authorization: Bearer <token>` but the TAUC API expects `X-Authorization: <token>`

**File:** `tauc_openapi/execute/auth_manager.py`

**Fix:** Changed line 88 from:
```python
headers['Authorization'] = f'Bearer {access_token}'
```
To:
```python
headers['X-Authorization'] = access_token
```

### 2. Missing Client Credentials in Token Request
**Issue:** The `GetAccessTokenRequest` didn't include `client_id` and `client_secret` needed for OAuth 2.0 client credentials flow.

**File:** `tauc_openapi/models/access_token/get_access_token.py`

**Fix:**
- Added `grant_type` field (defaults to "client_credentials")
- Changed content type to `application/x-www-form-urlencoded`
- Credentials are now dynamically added by ApiClient

### 3. ApiClient Not Sending Credentials
**Issue:** The `access_token_call` method wasn't adding client credentials to the token request.

**File:** `tauc_openapi/execute/api_client.py`

**Fix:** Modified `access_token_call` to inject `client_id` and `client_secret` into the request:
```python
if self.client_type == ClientType.OAUTH_TWO:
    if not self.client_id or not self.secret:
        raise TAUCApiException("Client ID and secret are required")
    setattr(request, 'client_id', self.client_id)
    setattr(request, 'client_secret', self.secret)
```

### 4. Form Encoding Improvements
**Issue:** Form-urlencoded body processing was too restrictive (strings only).

**File:** `tauc_openapi/base/request_utils.py`

**Fix:** Updated to handle all simple types (str, int, float, bool) and exclude special methods.

## Files Modified

| File | Lines Changed | Purpose |
|------|---------------|---------|
| `auth_manager.py` | 88 | Fixed OAuth header name |
| `get_access_token.py` | 10-27 | Added grant_type and form encoding |
| `api_client.py` | 160-168 | Inject client credentials |
| `request_utils.py` | 111-123 | Improved form encoding |

## Testing

After these fixes, the authentication flow works as follows:

### OAuth 2.0 Flow:
```python
# 1. Build client
client = ApiClient.build_oauth_client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    domain_name="https://api.tplinkcloud.com",
    client_cert_path="/path/to/client.crt",
    client_key_path="/path/to/client.key"
)

# 2. Get access token
token_request = GetAccessTokenRequest()
# ApiClient automatically adds client_id and client_secret
token_response = client.access_token_call(token_request, GetAccessTokenResponse)

# 3. Use the token
access_token = token_response.result.access_token
# Token is sent as: X-Authorization: <token>
response = client.api_call(some_request, SomeResponse, access_token)
```

### Request Details:

**Token Request:**
- Method: POST
- URL: `/v1/openapi/token`
- Content-Type: `application/x-www-form-urlencoded`
- Body: `grant_type=client_credentials&client_id=xxx&client_secret=xxx`

**Authenticated Request:**
- Headers: `X-Authorization: <access_token>`
- All other request parameters as normal

## Verification

To verify the fix works:

1. **Check SDK installation:**
```bash
cd /path/to/python-sdk
pip install -e .
```

2. **Test authentication:**
```python
from tauc_openapi import ApiClient
from tauc_openapi.models import GetAccessTokenRequest, GetAccessTokenResponse

client = ApiClient.build_oauth_client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    domain_name="https://api.tplinkcloud.com",
    client_cert_path="/path/to/certs/client.crt",
    client_key_path="/path/to/certs/client.key"
)

token_request = GetAccessTokenRequest()
token_response = client.access_token_call(token_request, GetAccessTokenResponse)

if token_response.is_success():
    print(f"✓ Authentication successful!")
    print(f"Access token: {token_response.result.access_token[:20]}...")
else:
    print(f"✗ Authentication failed: {token_response.msg}")
```

3. **Expected output:**
```
✓ Authentication successful!
Access token: eyJhbGciOiJIUzI1NiI...
```

## Common Errors After Fix

If you still encounter errors:

### Error: Certificate verify failed
**Cause:** Certificate paths are incorrect or certificates are invalid.
**Solution:** Verify certificate paths are absolute and files exist.

### Error: Invalid client credentials (Code: -70001)
**Cause:** Wrong client_id or client_secret.
**Solution:** Verify credentials with TP-Link.

### Error: Connection refused
**Cause:** Cannot reach API server.
**Solution:** Check network connectivity and API domain.

## Summary

The authentication system now correctly:
1. ✅ Sends OAuth tokens in `X-Authorization` header
2. ✅ Includes client credentials in token requests
3. ✅ Uses proper form-urlencoded format for token endpoint
4. ✅ Handles all request types correctly

These fixes align the Python SDK with the TAUC API requirements and match the behavior of the Java SDK.

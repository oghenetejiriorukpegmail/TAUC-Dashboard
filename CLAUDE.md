# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **TAUC Streamlit Dashboard**, a modern web-based UI for managing TP-Link network devices through the TAUC OpenAPI Python SDK (version 1.8.3). The application provides intuitive interfaces for inventory management, network operations, device lookups, service activation, and asset management.

**Technology Stack:**
- Python 3.7+
- Streamlit 1.28+
- TAUC OpenAPI Python SDK (installed from parent directory)
- Pandas (for data export)

## Essential Commands

### Setup and Installation
```bash
# Install TAUC SDK from parent directory (REQUIRED FIRST)
cd .. && pip install -e . && cd streamlit_app

# Install UI dependencies
pip install -r requirements.txt

# Set up environment (optional - creates .env from template)
./setup_env.sh
```

### Running the Application
```bash
# Smart launcher - auto-finds available port (8765-8800)
./run.sh

# Manual launch (fixed port)
streamlit run app.py --server.port=8765

# Custom port
streamlit run app.py --server.port=9000

# Port utilities
python port_helper.py              # Find available port
python port_helper.py check 8765   # Check if port is available
python port_helper.py list 8000 9000  # List used ports in range
```

### Development Workflow
```bash
# Check for import errors
python -c "from tauc_openapi import ApiClient; print('SDK OK')"

# Test authentication
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('TAUC_CLIENT_ID'))"
```

## Architecture Overview

### Application Structure

```
streamlit_app/
├── app.py                      # Main router with auth and navigation
├── pages/                      # Feature pages (modular)
│   ├── inventory.py           # View devices across all networks
│   ├── network_management.py  # NAT control, status, details
│   ├── device_lookup.py       # Find devices by SN/MAC
│   ├── service_activation.py  # Add/delete networks
│   └── asset_management.py    # Add/delete device assets
├── utils/                      # Reusable components
│   ├── ui_components.py       # UI display functions
│   └── api_helpers.py         # API call patterns
├── theme_css.py               # Dark/light theme styling
├── port_helper.py             # Port detection utility
└── .streamlit/config.toml     # Streamlit configuration
```

### Core Design Patterns

**1. Page Pattern (all pages follow this):**
```python
def show():
    """Main entry point called by app.py router."""
    # 1. Authentication check (optional but recommended)
    from utils import check_authentication
    if not check_authentication():
        return

    # 2. Page header
    st.title("Page Title")

    # 3. Tab-based layout (if multiple features)
    tab1, tab2 = st.tabs(["Feature 1", "Feature 2"])
    with tab1:
        feature_one_function()
    # ...
```

**2. API Call Pattern (use utils):**
```python
from utils import make_api_call, validate_response

# Make call with standard error handling
response = make_api_call(request, ResponseClass)

# Validate and display
if validate_response(response, "Success message!"):
    # Handle success - error already displayed if failed
    data = response.result
```

**3. Network Lookup Pattern:**
```python
from utils import get_network_by_name

# Searches across ALL network statuses (ONLINE, OFFLINE, etc.)
network_id, all_matches = get_network_by_name("NetworkName")
if network_id:
    # Found unique match
    proceed_with_operation(network_id)
```

### Session State Management

**Critical Session Variables:**
```python
st.session_state.authenticated  # bool: Authentication status
st.session_state.client         # ApiClient: SDK client instance
st.session_state.access_token   # str: OAuth token (None for AK/SK)
st.session_state.auth_type      # str: "OAuth 2.0" or "AK/SK"
st.session_state.theme          # str: "dark" or "light"
```

**Always check authentication:**
```python
if not st.session_state.get('client'):
    st.error("Not authenticated. Please login first.")
    return
```

## Critical Implementation Details

### 1. Zero-Indexed Pagination (CRITICAL)

The TAUC API uses **zero-indexed pagination**. This is a common source of bugs.

```python
# CORRECT - first page
request = GetNetworkNameListV2Request(
    page="0",        # First page is 0, not 1!
    pageSize="100",
    networkStatus="ONLINE"
)

# WRONG - will miss first page
request = GetNetworkNameListV2Request(page="1", ...)
```

### 2. Network Status Values (Must Use Strings)

```python
# CORRECT - string values
status = "ONLINE"    # or "OFFLINE", "ABNORMAL", "INVENTORY", "NAT-LOCKED", "SUSPEND"

# WRONG - numeric values DO NOT WORK
status = 0  # This will fail!
```

### 3. MAC Address Normalization

Always normalize MAC addresses before API calls:

```python
from utils import normalize_mac_address, validate_mac_address

# Handles: "AA:BB:CC:DD:EE:FF", "AA-BB-CC-DD-EE-FF", "aabbccddeeff"
# Output: "AABBCCDDEEFF"
clean_mac = normalize_mac_address(mac_input)

# Validate before proceeding
if not validate_mac_address(clean_mac, show_warning=True):
    return  # Warning already shown to user
```

### 4. Network Deletion Workflow

Networks must be deleted by ID, not name. Always look up first:

```python
from utils import get_network_by_name, make_api_call

# Step 1: Find network by name (searches all statuses)
network_id, matches = get_network_by_name("MyNetwork")

if not network_id:
    st.error("Network not found!")
    return

if len(matches) > 1:
    st.warning(f"Found {len(matches)} networks with that name!")
    # Show disambiguation UI

# Step 2: Delete by ID
from tauc_openapi.models import DeleteNetworkRequest, DeleteNetworkResponse
request = DeleteNetworkRequest(networkId=network_id)
response = make_api_call(request, DeleteNetworkResponse)
```

### 5. Authentication Flow

**OAuth 2.0 (Recommended):**
```python
from tauc_openapi import ApiClient
from tauc_openapi.models import GetAccessTokenRequest, GetAccessTokenResponse

# Build client with certificates
client = ApiClient.build_oauth_client(
    client_id=client_id,
    client_secret=client_secret,
    domain_name="https://api.tplinkcloud.com",
    client_cert_path="/absolute/path/to/certs/client.crt",
    client_key_path="/absolute/path/to/certs/client.key"
)

# Get access token
token_req = GetAccessTokenRequest()
token_resp = client.access_token_call(token_req, GetAccessTokenResponse)
access_token = token_resp.result.access_token

# Store in session
st.session_state.client = client
st.session_state.access_token = access_token
st.session_state.authenticated = True
```

**Access Key/Secret Key:**
```python
# Build client with AK/SK (no token needed)
client = ApiClient.build_aksk_client(
    access_key=access_key,
    secret_key=secret_key,
    domain_name="https://api.tplinkcloud.com",
    client_cert_path="/absolute/path/to/certs/client.crt",
    client_key_path="/absolute/path/to/certs/client.key"
)

# Store in session (access_token is None)
st.session_state.client = client
st.session_state.access_token = None
st.session_state.authenticated = True
```

## Utils Module Functions

### UI Components (utils/ui_components.py)

**Display Functions:**
```python
from utils import (
    display_api_response,      # Show API response in expandable JSON
    display_export_buttons,    # CSV/JSON download buttons
    display_network_table,     # Format network data as table
    display_error_message,     # Error display with solutions
    display_success_message,   # Success notification
    display_metrics_row,       # Dashboard metric cards
    display_info_card,         # Info card component
    display_loading_spinner    # Context manager for loading
)

# Example usage
display_api_response(response, endpoint="/v1/openapi/...")
display_export_buttons(data=networks, filename_prefix="networks", key_prefix="export")
display_error_message(error_code=-70325, message="Validation failed")
```

### API Helpers (utils/api_helpers.py)

**API Functions:**
```python
from utils import (
    make_api_call,              # Execute API call with error handling
    validate_response,          # Check response and display messages
    get_network_by_name,        # Look up network ID by name
    get_all_networks,           # Fetch all networks across statuses
    batch_delete_with_progress, # Delete with progress bar
    check_authentication,       # Verify auth status
    normalize_mac_address,      # Convert MAC to standard format
    validate_mac_address        # Validate MAC format
)
```

## Adding New Features

### Adding a New Page

1. **Create page module** in `pages/new_feature.py`:
```python
import streamlit as st
from utils import make_api_call, validate_response, check_authentication

def show():
    """New feature page entry point."""
    if not check_authentication():
        return

    st.title("New Feature")
    # Implementation here
```

2. **Register in app.py** (around line 200+):
```python
from pages import new_feature

# In main() function:
elif page == "New Feature":
    new_feature.show()
```

3. **Add to sidebar navigation** in `main()`:
```python
menu_options = [
    "Home",
    "Inventory",
    # ... existing pages ...
    "New Feature"  # Add here
]
```

### Adding New API Endpoints

If the SDK already has the request/response models:

```python
# 1. Import models
from tauc_openapi.models import NewFeatureRequest, NewFeatureResponse

# 2. Use in page
from utils import make_api_call, validate_response

def execute_new_feature():
    request = NewFeatureRequest(param="value")
    response = make_api_call(request, NewFeatureResponse)

    if validate_response(response, "Feature executed successfully!"):
        # Handle result
        result = response.result
```

If the SDK doesn't have the models, refer to parent directory's `CLAUDE.md` for instructions on adding SDK models.

## Common Patterns and Conventions

### Form Submission Pattern
```python
with st.form("unique_form_key"):
    field1 = st.text_input("Label")
    field2 = st.number_input("Number")

    submitted = st.form_submit_button("Submit", type="primary")
    if submitted:
        # Validation
        if not field1:
            st.error("Field is required!")
            return

        # API call
        response = make_api_call(request, ResponseClass)
        if validate_response(response, "Success!"):
            # Handle success
            pass
```

### Export Data Pattern
```python
# Prepare data for export (list of dicts)
export_data = [
    {
        "id": item.id,
        "name": item.name,
        "status": item.status
    }
    for item in items
]

# Display export buttons (CSV + JSON)
display_export_buttons(
    data=export_data,
    filename_prefix="tauc_items",
    key_prefix="items_export"
)
```

### Batch Operation Pattern
```python
from utils import batch_delete_with_progress

# Define delete function for a single item
def delete_single_network(network_id):
    request = DeleteNetworkRequest(networkId=network_id)
    response = make_api_call(request, DeleteNetworkResponse)
    return response.is_success() if response else False

# Execute batch deletion with progress bar
result = batch_delete_with_progress(
    items=networks_to_delete,
    delete_function=delete_single_network,
    item_name_key="network_name",
    item_id_key="id"
)

st.info(f"Deleted {result['success_count']}/{result['total']} networks")
```

## Configuration and Environment

### Environment Variables (.env)
```bash
# OAuth 2.0 credentials
TAUC_CLIENT_ID=your_client_id
TAUC_CLIENT_SECRET=your_client_secret

# OR Access Key/Secret Key credentials
TAUC_ACCESS_KEY=your_access_key
TAUC_SECRET_KEY=your_secret_key

# Optional metadata
TAUC_OPERATOR_NAME=YourName
TAUC_ENV=Production
TAUC_ACCOUNT_EMAIL=user@example.com
```

### Certificate Paths
Certificates are required for mTLS authentication and must be **absolute paths**:

```python
# Default locations (relative to streamlit_app/)
cert_path = "../certs/client.crt"
key_path = "../certs/client.key"

# Convert to absolute paths
import os
cert_path = os.path.abspath(cert_path)
key_path = os.path.abspath(key_path)
```

### Streamlit Configuration (.streamlit/config.toml)
```toml
[server]
headless = true                    # No auto-open browser
port = 8765                        # Default port (overridden by run.sh)
enableCORS = false                 # Security
enableXsrfProtection = true        # XSRF protection

[theme]
primaryColor = "#00BCD4"           # Teal accent (TP-Link official)
backgroundColor = "#1a1a1a"        # Dark mode background
textColor = "#FAFAFA"              # Light text

[client]
showSidebarNavigation = false      # Custom sidebar
toolbarMode = "minimal"

[runner]
fastReruns = true                  # Performance
```

## Theme System

The app supports dark/light themes with custom CSS:

```python
# Theme stored in session
st.session_state.theme = 'dark'  # or 'light'

# Get theme colors for inline styles
from app import get_theme_colors
colors = get_theme_colors(st.session_state.theme)

# Use in custom HTML
st.markdown(f"""
<div style='color: {colors["text_primary"]};'>
    Content here
</div>
""", unsafe_allow_html=True)
```

**Custom CSS Classes** (defined in theme_css.py):
- `.tauc-hero`: Hero banner with gradient
- `.tauc-card`: Information card with border
- `.tauc-divider`: Visual separator
- `.tauc-chip`: Small tag/label component
- `.tauc-status-card`: Status indicator
- `.metric-card`: Dashboard metric display

## Troubleshooting Common Issues

### Issue: Empty Results from API
**Cause:** Using `page="1"` instead of `page="0"`
**Solution:** Always use `page="0"` for first page

### Issue: Network Status Query Fails
**Cause:** Using numeric status values (0, 1, etc.) instead of strings
**Solution:** Use string values: `"ONLINE"`, `"OFFLINE"`, etc.

### Issue: MAC Address Not Found
**Cause:** MAC format mismatch (colons vs no separator)
**Solution:** Use `normalize_mac_address()` before API calls

### Issue: Network Not Found for Deletion
**Cause:** Network exists but in different status than queried
**Solution:** Use `get_network_by_name()` which searches all statuses

### Issue: Port Already in Use
**Cause:** Port 8765 occupied by another service
**Solution:** Use `./run.sh` for auto-detection or `streamlit run app.py --server.port=XXXX`

### Issue: SDK Import Error
**Cause:** SDK not installed from parent directory
**Solution:** `cd .. && pip install -e . && cd streamlit_app`

### Issue: Certificate Not Found
**Cause:** Relative paths don't resolve correctly
**Solution:** Use absolute paths: `os.path.abspath("../certs/client.crt")`

## Error Code Reference

Common TAUC API error codes:

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 0 | Success | No action needed |
| -70325 | Parameter Validation Failed | Check parameters match API spec |
| -70346 | Invalid Parameter | Verify parameter types and format |
| -70435 | Access Token Expired | Re-authenticate (logout → login) |
| -40310 | Resource Not Found | Verify IDs are correct |

See `display_error_message()` in `utils/ui_components.py` for comprehensive error handling.

## Best Practices

### DO:
- ✅ Use utils functions (`make_api_call`, `validate_response`, etc.)
- ✅ Always use `page="0"` for first page
- ✅ Normalize MAC addresses with `normalize_mac_address()`
- ✅ Check authentication at page entry with `check_authentication()`
- ✅ Use `display_api_response()` to show raw API responses
- ✅ Use `display_export_buttons()` for CSV/JSON downloads
- ✅ Handle errors with `validate_response()` or `display_error_message()`
- ✅ Use absolute paths for certificates
- ✅ Store credentials in `.env` (never commit!)
- ✅ Use string network status values (`"ONLINE"`, not `0`)

### DON'T:
- ❌ Don't implement custom API call error handling (use utils)
- ❌ Don't use `page="1"` for first page (use `page="0"`)
- ❌ Don't use numeric network status values (use strings)
- ❌ Don't assume MAC format (always normalize)
- ❌ Don't query single status for network lookup (use `get_network_by_name()`)
- ❌ Don't commit `.env` or certificates
- ❌ Don't use relative certificate paths in production
- ❌ Don't duplicate UI components (use utils)

## Performance Considerations

- **Pagination:** Use appropriate page sizes (25-100) to balance performance and usability
- **Batch Operations:** Use `batch_delete_with_progress()` for operations on multiple items
- **Caching:** Streamlit reruns on every interaction; avoid expensive operations in main flow
- **Network Queries:** `get_all_networks()` queries 6 statuses sequentially - use sparingly

## Security Notes

- **Credentials:** Never commit `.env` file or certificates to version control
- **Session State:** Auth credentials stored only in session (lost on browser refresh)
- **HTTPS:** Enable in production deployments
- **CORS:** Disabled by default for security
- **XSRF Protection:** Enabled by default

## Related Documentation

For comprehensive information, see:
- **ARCHITECTURE.md**: Detailed architecture and data flow
- **README.md**: User guide and installation instructions
- **AGENTS.md**: Repository guidelines and commit conventions
- **Parent CLAUDE.md** (`../CLAUDE.md`): SDK-level documentation

For SDK model details and adding new API endpoints to the SDK itself, refer to the parent directory's CLAUDE.md documentation.

# Streamlit App Architecture

## Overview

The TAUC Streamlit Dashboard is a web-based UI for managing TP-Link network devices via the TAUC OpenAPI. The application follows a modular architecture with clear separation of concerns.

## Directory Structure

```
streamlit_app/
├── app.py                  # Main application entry point
├── pages/                  # Page modules
│   ├── __init__.py
│   ├── inventory.py       # Inventory management
│   ├── network_management.py  # Network operations
│   ├── device_lookup.py   # Device information lookup
│   ├── service_activation.py  # Network provisioning
│   └── asset_management.py    # Asset management
├── utils/                  # Shared utilities (NEW)
│   ├── __init__.py
│   ├── ui_components.py   # Reusable UI components
│   └── api_helpers.py     # Common API patterns
├── .streamlit/            # Streamlit configuration
│   └── config.toml
├── .env                   # Environment variables
└── run.sh                 # Launch script

```

## Architecture Principles

### 1. Modularity
- Each page is a separate module with a `show()` function
- Shared functionality extracted to utils modules
- No circular dependencies

### 2. Separation of Concerns
- **app.py**: Routing and authentication
- **pages/**: Feature-specific UI and logic
- **utils/**: Reusable components and helpers

### 3. Consistency
- Standardized error handling across all pages
- Unified API response display
- Common UI patterns (export buttons, metrics, etc.)

## Core Components

### Main Application (app.py)

**Responsibilities:**
- Session state initialization
- Authentication management (OAuth 2.0 and AK/SK)
- Page routing
- Sidebar navigation

**Session State:**
```python
{
    'authenticated': bool,
    'client': ApiClient,
    'access_token': str,
    'auth_type': str  # "OAuth 2.0" or "AK/SK"
}
```

### Page Modules (pages/)

Each page module follows this pattern:

```python
def show():
    """Main entry point for the page."""
    st.title("Page Title")
    # Page content here
```

**Current Pages:**
1. **Home**: Dashboard with quick stats
2. **Inventory**: View and manage device inventory
3. **Network Management**: NAT lock/unlock, network details
4. **Device Lookup**: Find devices by SN/MAC
5. **Service Activation**: Provision networks (add/delete)
6. **Asset Management**: Manage device assets (add/delete)

### Utils Module (utils/)

#### ui_components.py

**Reusable UI Functions:**

```python
# API Response Display
display_api_response(response, endpoint, show_full_data=False)

# Export Functionality
display_export_buttons(data, filename_prefix, key_prefix)

# Network Display
display_network_table(networks, show_actions=False)

# Error/Success Messages
display_error_message(error_code, message, show_common_solutions=True)
display_success_message(message, details=None)

# Metrics
display_metrics_row(metrics)

# Loading
display_loading_spinner(text="Processing...")
```

**Benefits:**
- Consistent UI across all pages
- Reduced code duplication
- Centralized error message handling with solutions
- Easy to update UI patterns globally

#### api_helpers.py

**Common API Patterns:**

```python
# Standard API Call
make_api_call(request, response_class, access_token=None,
              show_spinner=True, spinner_text="Processing...")

# Response Validation
validate_response(response, success_message=None, show_errors=True)

# Network Lookup
get_network_by_name(network_name, page_size="100", case_sensitive=False)

# Fetch All Networks
get_all_networks(page_size="100", status_filter=None)

# Batch Operations
batch_delete_with_progress(items, delete_function, item_name_key, item_id_key)

# Authentication Check
check_authentication()
```

**Benefits:**
- Consistent error handling
- Reduced code duplication
- Centralized authentication checks
- Progress tracking for batch operations

## Data Flow

### Authentication Flow

```
User -> Configuration Page
  -> Select Auth Method (OAuth 2.0 or AK/SK)
  -> Enter Credentials
  -> ApiClient.build_*_client()
  -> Store in session_state
  -> Get Access Token (OAuth only)
  -> Redirect to Home
```

### API Call Flow

```
Page -> make_api_call(request, response_class)
  -> Check authentication
  -> Execute API call
  -> validate_response()
  -> Display result or error
  -> (Optional) display_api_response()
```

### Network Deletion Flow

```
User Input (Network Name)
  -> get_network_by_name()
  -> Query all statuses (ONLINE, OFFLINE, etc.)
  -> Match network name
  -> Get network ID
  -> DeleteNetworkRequest
  -> make_api_call()
  -> Display success/error
```

## API Integration

### TAUC API Response Pattern

All responses follow this structure:

```json
{
  "errorCode": 0,
  "msg": "success",
  "result": {
    "total": 100,
    "page": 0,
    "pageSize": 25,
    "data": [...]
  }
}
```

### Zero-Indexed Pagination

**Important**: The TAUC API uses zero-indexed pagination:
- `page=0` is the first page
- `page=1` is the second page

All code has been updated to use `page="0"` consistently.

### Network Status Values

The API uses string status values:
- `"ONLINE"`: Network is operational
- `"OFFLINE"`: Network is not reachable
- `"ABNORMAL"`: Network has issues
- `"INVENTORY"`: Network in inventory status
- `"NAT-LOCKED"`: Network is locked
- `"SUSPEND"`: Network is suspended

## Best Practices

### 1. Error Handling

Always use `validate_response()` or check `response.is_success()`:

```python
response = make_api_call(request, ResponseClass)
if validate_response(response, "Operation successful!"):
    # Handle success
    pass
```

### 2. API Responses

Use `display_api_response()` for consistency:

```python
display_api_response(
    response,
    endpoint="/v1/openapi/endpoint",
    show_full_data=True
)
```

### 3. Export Functionality

Use `display_export_buttons()` instead of custom implementations:

```python
display_export_buttons(
    data=networks_list,
    filename_prefix="tauc_networks",
    key_prefix="networks_export"
)
```

### 4. Network Lookups

Use `get_network_by_name()` or `get_all_networks()`:

```python
# Find specific network
network_id, matches = get_network_by_name("MyNetwork")

# Get all networks
all_networks = get_all_networks(status_filter="ONLINE")
```

## Future Improvements

### Potential Enhancements:

1. **Caching Layer**
   - Cache network lists to reduce API calls
   - Implement cache invalidation on updates

2. **Async Operations**
   - Use asyncio for parallel API calls
   - Improve performance for batch operations

3. **Advanced Filtering**
   - Add search/filter across all tables
   - Implement sorting by column

4. **Export Enhancements**
   - Add Excel export option
   - Support exporting filtered data only

5. **Logging**
   - Add comprehensive logging
   - Track API call history

6. **Testing**
   - Unit tests for utils modules
   - Integration tests for API calls
   - UI tests for critical flows

7. **State Management**
   - Consider using st.cache for expensive operations
   - Implement proper state cleanup on logout

## Configuration

### Environment Variables (.env)

```bash
# OAuth 2.0
TAUC_CLIENT_ID=your_client_id
TAUC_CLIENT_SECRET=your_client_secret

# OR Access Key/Secret Key
TAUC_ACCESS_KEY=your_access_key
TAUC_SECRET_KEY=your_secret_key
```

### Streamlit Config (.streamlit/config.toml)

```toml
[server]
headless = true
# Port is set via command line in run.sh
enableCORS = false
enableXsrfProtection = true

[theme]
primaryColor = "#FF6B00"
backgroundColor = "#FFFFFF"
```

## Deployment

### Local Development

```bash
# Navigate to streamlit_app directory
cd streamlit_app

# Run with automatic port detection
./run.sh

# Or specify port manually
streamlit run app.py --server.port=8765
```

### Production Considerations

1. **Security**
   - Never commit `.env` file
   - Use secrets management (st.secrets)
   - Enable HTTPS in production

2. **Performance**
   - Use caching where appropriate
   - Implement pagination for large datasets
   - Consider connection pooling

3. **Monitoring**
   - Add logging
   - Track error rates
   - Monitor API response times

## Troubleshooting

### Common Issues

**1. Authentication Failed**
- Check credentials in .env
- Verify certificate paths
- Ensure API endpoint is correct

**2. Empty Data Returns**
- Verify using `page="0"` not `page="1"`
- Check network status filter
- Verify account has access to resources

**3. Port Already in Use**
- run.sh automatically finds available port
- Or manually specify: `streamlit run app.py --server.port=XXXX`

**4. Import Errors**
- Ensure SDK is installed: `pip install -e ..`
- Check virtual environment is activated
- Verify all dependencies installed

## Code Quality

### Metrics

- **Total Lines**: ~2,900 (app + pages + utils)
- **Modules**: 10 Python files
- **Reusable Functions**: 15+ in utils/
- **Pages**: 6 functional pages
- **API Endpoints Supported**: 20+

### Maintainability Features

- Clear module separation
- Consistent naming conventions
- Comprehensive docstrings
- Type hints where applicable
- DRY principle (Don't Repeat Yourself)
- Single Responsibility Principle
- Open/Closed Principle (extensible)

## Contributing

When adding new features:

1. Create page module in `pages/`
2. Use utils functions for common patterns
3. Follow existing code style
4. Add docstrings
5. Test thoroughly
6. Update this documentation

## Version History

- **v1.0.0**: Initial release with basic features
- **v1.1.0**: Added Service Activation and Asset Management
- **v1.2.0**: Added utils module for code reusability
- **v1.2.1**: Fixed pagination (0-indexed) and status values
- **v1.2.2**: Removed hardcoded port, improved run.sh

# TAUC Device Management Dashboard

A web-based user interface for managing TP-Link network devices through the TAUC OpenAPI. Built with Streamlit for easy deployment and use.

**Cross-Platform:** Works on Windows, Linux, and macOS with dedicated launchers for each platform.

![Dashboard Preview](https://img.shields.io/badge/Status-Beta-yellow)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)

## Features

### 🔑 Authentication
- **Dual Authentication Support**: OAuth 2.0 and Access Key/Secret Key (AK/SK)
- **Secure Session Management**: Credentials stored only in session state
- **Easy Configuration**: Simple web form for credential input

### 📦 Inventory Management
- **View All Devices**: Paginated view of all registered devices
- **NAT-Locked Devices**: Specialized view for suspended devices
- **Export to CSV**: Download inventory data for offline analysis
- **Network Grouping**: Devices organized by network
- **Rich Device Details**: Serial numbers, MAC addresses, models, firmware versions

### 🔧 Network Management
- **NAT Control**: Lock/unlock NAT to suspend/resume networks
- **Network Status**: Real-time network status checking
- **Network Details**: Comprehensive network information with all devices
- **CSV Export**: Export network device lists

### 🔍 Device Lookup
- **MAC Address Lookup**: Find device ID by MAC address
- **Serial Number Lookup**: Find device ID by serial number
- **Detailed Device Info**: View all available device information
- **Copy-friendly Output**: Easy to copy device IDs and details

## Installation

### Prerequisites
- Python 3.7 or higher
- TAUC OpenAPI Python SDK (installed from parent directory)
- Valid TAUC API credentials (OAuth or AK/SK)
- Client certificate and key files

### Quick Start (Linux/Mac)

1. **Install the TAUC SDK** (from parent directory):
   ```bash
   cd ..
   pip install -e .
   ```

2. **Install UI dependencies**:
   ```bash
   cd streamlit_app
   pip install -r requirements.txt
   ```

3. **Run the dashboard**:
   ```bash
   ./run.sh          # Smart launcher with auto port detection
   ```

   Or manually specify the command:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**:

### Quick Start (Windows)

1. **Install the TAUC SDK** (from parent directory):
   ```cmd
   cd ..
   pip install -e .
   ```

2. **Install UI dependencies**:
   ```cmd
   cd streamlit_app
   pip install -r requirements.txt
   ```

3. **Run the dashboard**:
   ```cmd
   run.bat           # Smart launcher with auto port detection
   ```

   Or manually specify the command:
   ```cmd
   streamlit run app.py
   ```

4. **Open your browser**:
   - The dashboard will start on port 8765 by default (or next available port)
   - Navigate to the URL shown in your terminal (e.g., `http://localhost:8765`)
   - The launcher scripts automatically avoid port conflicts with Docker containers

## Usage

### First Time Setup

1. **Launch the Dashboard**:
   ```bash
   streamlit run app.py
   ```

2. **Configure Authentication**:
   - Select authentication method (OAuth 2.0 or AK/SK)
   - Enter your credentials
   - Specify certificate paths (defaults to `../certs/`)
   - Click "Authenticate"

3. **Start Managing Devices**:
   - Use the sidebar to navigate between sections
   - View inventory, manage networks, or lookup devices

### Authentication Methods

#### OAuth 2.0 (Recommended)
```
Client ID: your_client_id
Client Secret: your_client_secret
Domain: https://api.tplinkcloud.com
Certificate Path: /path/to/certs/client.crt
Key Path: /path/to/certs/client.key
```

#### Access Key/Secret Key
```
Access Key: your_access_key
Secret Key: your_secret_key
Domain: https://api.tplinkcloud.com
Certificate Path: /path/to/certs/client.crt
Key Path: /path/to/certs/client.key
```

### Certificate Setup

The dashboard requires the mTLS certificates located in the `certs/` directory:
- `client.crt`: Client certificate
- `client.key`: Private key

By default, the dashboard looks for certificates at:
```
/home/user/Documents/Tplink/TAUC/1.8.3/python-sdk/certs/
```

Update the paths in the configuration page if your certificates are elsewhere.

## Features Guide

### 📦 Inventory Management

**View All Inventory:**
1. Navigate to "Inventory" → "All Inventory" tab
2. Set page number and page size
3. Click "Fetch Inventory"
4. Expand networks to see devices
5. Export individual networks or all data to CSV

**View NAT-Locked Devices:**
1. Navigate to "Inventory" → "NAT-Locked Devices" tab
2. Set pagination parameters
3. Click "Fetch NAT-Locked"
4. View suspended devices grouped by network

### 🔧 Network Management

**Lock/Unlock NAT:**
1. Navigate to "Network Management" → "NAT Control" tab
2. Enter Network ID
3. Click "Lock NAT" to suspend or "Unlock NAT" to resume

**Check Network Status:**
1. Navigate to "Network Management" → "Network Status" tab
2. Enter Network ID
3. Click "Get Status"
4. View current status and details

**View Network Details:**
1. Navigate to "Network Management" → "Network Details" tab
2. Enter Network ID
3. Click "Get Details"
4. View comprehensive network info and all devices
5. Export devices to CSV

### 🔍 Device Lookup

**Lookup by MAC Address:**
1. Navigate to "Device Lookup"
2. Select "By MAC Address"
3. Enter MAC address (format: AA:BB:CC:DD:EE:FF)
4. Click "Search"
5. View device ID and details

**Lookup by Serial Number:**
1. Navigate to "Device Lookup"
2. Select "By Serial Number"
3. Enter serial number
4. Click "Search"
5. View device ID and details

## Project Structure

```
streamlit_app/
├── app.py                      # Main application entry point
├── pages/                      # Page modules
│   ├── __init__.py            # Pages package init
│   ├── inventory.py           # Inventory management page
│   ├── network_management.py  # Network management page
│   └── device_lookup.py       # Device lookup page
├── requirements.txt           # UI dependencies
└── README.md                  # This file
```

## Port Management

The dashboard includes intelligent port management to avoid conflicts with Docker containers and other services.

### Automatic Port Selection

The launcher scripts (`run.sh` / `run.bat`) automatically:
1. Check if port 8765 is available
2. If in use, try ports 8766, 8767, etc. up to 8800
3. Display the selected port in the terminal
4. Launch the dashboard on the first available port

### Manual Port Selection

To use a specific port:
```bash
streamlit run app.py --server.port=9000
```

### Default Port Configuration

The default port is set in `.streamlit/config.toml`:
```toml
[server]
port = 8765
```

You can change this, but the launcher scripts will override it to find an available port.

## Configuration

### Session State Variables

The dashboard uses Streamlit session state to manage:
- `authenticated`: Authentication status
- `client`: ApiClient instance
- `access_token`: OAuth access token (if using OAuth)
- `auth_type`: Authentication method in use

### Default Settings

- **API Domain**: `https://api.tplinkcloud.com`
- **Certificate Path**: `../certs/client.crt`
- **Key Path**: `../certs/client.key`
- **Page Size**: 25 items per page
- **Default Port**: 8765 (automatically finds next available if in use)
- **Port Range**: 8765-8800 (for automatic selection)

### Customization

To change default settings, edit `app.py`:

```python
# Change default domain
domain_name = st.text_input("API Domain", value="https://custom.domain.com")

# Change default certificate paths
default_cert = "/custom/path/to/client.crt"
default_key = "/custom/path/to/client.key"
```

## Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Production Deployment

For production use, consider:

1. **Streamlit Cloud**:
   ```bash
   # Push to GitHub and connect via Streamlit Cloud
   # https://streamlit.io/cloud
   ```

2. **Docker**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . .
   RUN pip install -e .. && pip install -r requirements.txt
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.port=8501"]
   ```

3. **Custom Server**:
   ```bash
   streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

## Troubleshooting

### Common Issues

**Certificate Not Found**:
```
Error: [Errno 2] No such file or directory: '/path/to/client.crt'
```
**Solution**: Update certificate paths in the configuration page to absolute paths.

**Authentication Failed**:
```
Error: Authentication failed: Invalid credentials (Code: -70001)
```
**Solution**: Verify your Client ID/Secret or Access Key/Secret Key are correct.

**Import Error**:
```
ModuleNotFoundError: No module named 'tauc_openapi'
```
**Solution**: Install the TAUC SDK from parent directory:
```bash
cd .. && pip install -e . && cd streamlit_app
```

**Connection Error**:
```
Error: Connection refused
```
**Solution**: Check that the API domain is correct and accessible. Verify network connectivity.

### Debug Mode

To see detailed error information, check the Streamlit terminal output or expand the "Debug Information" sections in error messages.

## Limitations

- **Read-Only for Some Operations**: Currently implements only the models available in the SDK
- **Session-Based Auth**: Credentials not persisted between sessions
- **No Multi-User Support**: Single-user dashboard (each browser session is independent)
- **Certificate Paths**: Must be absolute paths, relative paths may not work correctly

## Future Enhancements

- [ ] Bulk device lookup (upload CSV)
- [ ] Real-time device monitoring
- [ ] Network topology visualization
- [ ] Historical data and analytics
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Scheduled reports
- [ ] Device grouping and tagging
- [ ] Firmware update management
- [ ] WiFi configuration interface

## Support

For issues and questions:
- Check the [main SDK README](../README.md)
- Review [CLAUDE.md](../CLAUDE.md) for architecture details
- File issues on the project repository

## License

Copyright © 2022-2025 TP-Link Technologies Co., Ltd. All rights reserved.

## Version

Dashboard Version: 1.0.0
SDK Version: 1.8.3

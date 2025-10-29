# TAUC Dashboard - Quick Reference Card

## 🚀 Quick Start
```bash
./run.sh                    # Linux/Mac (auto port detection)
run.bat                     # Windows (auto port detection)
streamlit run app.py        # Manual (uses port 8765)
```

## 🔌 Port Management
```bash
python3 port_helper.py              # Find available port
python3 port_helper.py check 8765   # Check if port free
python3 port_helper.py list 8000 9000   # Show used ports
```

**Default Port:** 8765 (auto-increments if busy)
**Port Range:** 8765-8800 (automatic selection)

## 📁 File Structure
```
streamlit_app/
├── app.py                    # Main dashboard (config + routing)
├── pages/
│   ├── inventory.py          # View all/NAT-locked devices
│   ├── network_management.py # Lock/unlock, status, details
│   └── device_lookup.py      # Search by MAC/SN
├── port_helper.py            # Port management utility
├── run.sh / run.bat          # Smart launchers
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── QUICKSTART.md             # Quick start guide
└── PORT_MANAGEMENT.md        # Port configuration details
```

## 🎯 Main Features

### 📦 Inventory Page
- **All Inventory**: View all registered devices (paginated)
- **NAT-Locked**: View suspended/locked devices
- **Export**: Download CSV for any view

### 🔧 Network Management Page
- **NAT Control**: Lock/unlock networks
- **Status**: Check network status by ID
- **Details**: View full network info + device list

### 🔍 Device Lookup Page
- **By MAC**: Find device ID using MAC address
- **By SN**: Find device ID using serial number

## 🔐 Authentication

### OAuth 2.0
```
Client ID: your_client_id
Client Secret: your_client_secret
Domain: https://api.tplinkcloud.com
Cert: /path/to/certs/client.crt
Key: /path/to/certs/client.key
```

### Access Key/Secret Key
```
Access Key: your_access_key
Secret Key: your_secret_key
Domain: https://api.tplinkcloud.com
Cert: /path/to/certs/client.crt
Key: /path/to/certs/client.key
```

## 📊 API Endpoints Implemented

| Feature | Request | Response |
|---------|---------|----------|
| Get Access Token | GetAccessTokenRequest | GetAccessTokenResponse |
| All Inventory | GetAllInventoryRequest | GetAllInventoryResponse |
| NAT-Locked Inventory | GetNATLockedInventoryRequest | GetNATLockedInventoryResponse |
| Lock NAT | NATLockMeshControllerRequest | NATLockMeshControllerResponse |
| Unlock NAT | NATUnlockMeshControllerRequest | NATUnlockMeshControllerResponse |
| Network Status | GetNetworkStatusRequest | GetNetworkStatusResponse |
| Network Details | GetNetworkDetailsRequest | GetNetworkDetailsResponse |
| Device ID Lookup | GetDeviceIdRequest | GetDeviceIdResponse |

## 🛠️ Common Commands

### Installation
```bash
pip install -r requirements.txt
cd .. && pip install -e . && cd streamlit_app
```

### Launch
```bash
./run.sh                              # Auto port selection
streamlit run app.py                  # Default port 8765
streamlit run app.py --server.port=9000   # Custom port
```

### Port Management
```bash
python3 port_helper.py                # Find free port
python3 port_helper.py check 8765     # Check specific port
python3 port_helper.py find 9000 9100 # Find in range
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | Run `./run.sh` (auto-selects next port) |
| Module not found | `cd .. && pip install -e .` |
| Cert not found | Use absolute paths in config page |
| Auth failed | Verify credentials are correct |
| Connection refused | Check API domain and network |

## 🔗 Navigation Flow

```
Launch → Configuration Page (if not authenticated)
                ↓
         Authenticate (OAuth/AK-SK)
                ↓
         Home Dashboard
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
Inventory   Network    Device
           Management  Lookup
```

## 📝 Session State

- `authenticated`: Bool (auth status)
- `client`: ApiClient instance
- `access_token`: OAuth token (if OAuth)
- `auth_type`: "OAuth 2.0" or "AK/SK"

## 🎨 Customization Points

### Change Default Port
Edit `.streamlit/config.toml`:
```toml
[server]
port = 9000
```

### Change Certificate Paths
Edit `app.py` line ~95:
```python
default_cert = "/your/path/client.crt"
default_key = "/your/path/client.key"
```

### Change API Domain Default
Edit `app.py` line ~85:
```python
domain_name = st.text_input("API Domain", value="https://custom.domain.com")
```

## 📌 Key Files to Edit

| Task | File | Line(s) |
|------|------|---------|
| Add new page | `app.py` | ~35 (navigation), ~50 (routing) |
| Modify auth | `app.py` | ~100-200 (auth functions) |
| Change defaults | `app.py` | ~85-100 (config page) |
| Add SDK endpoint | `pages/*.py` | Import new models, add to UI |
| Port config | `.streamlit/config.toml` | line 10 |
| Port range | `run.sh` / `run.bat` | lines 42-44 |

## 📚 Documentation Files

- `README.md` - Complete documentation
- `QUICKSTART.md` - Quick start guide (3 steps)
- `PORT_MANAGEMENT.md` - Port configuration details
- `QUICK_REFERENCE.md` - This file
- `../CLAUDE.md` - SDK architecture & patterns

## ⚡ Performance Tips

1. Use pagination (don't fetch all data at once)
2. Close client after use (or use context manager)
3. Cache access token during session
4. Export to CSV for large datasets

## 🌐 URLs & Ports

- **Dashboard**: http://localhost:8765 (or shown in terminal)
- **API Endpoint**: https://api.tplinkcloud.com
- **Port Range**: 8765-8800 (auto-select)

## 💡 Pro Tips

1. **Multiple Instances**: Each `./run.sh` uses next available port
2. **Export Data**: All inventory/network views have CSV export
3. **Port Helper**: Run before launch to verify port availability
4. **Logout**: Use sidebar button to re-configure credentials
5. **Error Messages**: Expand "Debug Information" for details

---

**Need More Help?**
- Full docs: `README.md`
- Quick start: `QUICKSTART.md`
- Port issues: `PORT_MANAGEMENT.md`
- SDK details: `../CLAUDE.md`

# Quick Start Guide

Get the TAUC Dashboard running in 3 simple steps!

## Step 0: Setup Credentials (Optional but Recommended)

Create a `.env` file to store your credentials:

```bash
# Quick setup (interactive)
./setup_env.sh

# Or manual setup
cp .env.example .env
nano .env  # Add your TAUC_CLIENT_ID and TAUC_CLIENT_SECRET
```

**.env file format:**
```bash
TAUC_CLIENT_ID=your_client_id_here
TAUC_CLIENT_SECRET=your_client_secret_here
```

**Important:** The .env file is automatically ignored by git to protect your credentials!

## Step 1: Install Dependencies

```bash
# From the streamlit_app directory
pip install -r requirements.txt

# Install the TAUC SDK (with authentication fixes)
cd .. && pip install -e . && cd streamlit_app
```

> **Note:** Recent fixes resolve the "X-Authorization header info is empty (Code: -70411)" error. Make sure to reinstall the SDK to pick up these fixes!

## Step 2: Prepare Certificates

Make sure you have the required certificates:
- `../certs/client.crt` - Client certificate
- `../certs/client.key` - Private key

## Step 3: Launch Dashboard

### Linux/Mac:
```bash
./run.sh
```

### Windows:
```cmd
run.bat
```

### Manual:
```bash
streamlit run app.py
```

## Step 4: Configure & Use

1. **Open Browser**: The launcher will tell you which port is being used (default: 8765)
   - Navigate to `http://localhost:8765` (or the port shown in the terminal)

2. **Authenticate**:
   - Choose OAuth 2.0 or AK/SK
   - Enter your credentials
   - Verify certificate paths
   - Click "Authenticate"

3. **Start Managing**:
   - 📦 **Inventory**: View all devices and NAT-locked devices
   - 🔧 **Network Management**: Lock/unlock NAT, view status
   - 🔍 **Device Lookup**: Find devices by MAC or Serial Number

## Troubleshooting

**Check which port will be used:**
```bash
python port_helper.py
```

**Port already in use?**
The launcher scripts automatically find an available port (8765-8800).
If you want to use a specific port:
```bash
streamlit run app.py --server.port=9000
```

**Check if a specific port is available:**
```bash
python port_helper.py check 8765
```

**Find available port in custom range:**
```bash
python port_helper.py find 9000 9100
```

**List all used ports in a range:**
```bash
python port_helper.py list 8000 9000
```

**Module not found?**
```bash
# Make sure SDK is installed
cd .. && pip install -e .
```

**Certificate errors?**
- Use absolute paths in the configuration page
- Verify certificates exist and have correct permissions

## Features at a Glance

| Feature | Description | Tab/Page |
|---------|-------------|----------|
| View All Inventory | See all registered devices | Inventory → All Inventory |
| NAT-Locked Devices | View suspended devices | Inventory → NAT-Locked |
| Lock NAT | Suspend a network | Network → NAT Control |
| Unlock NAT | Resume a network | Network → NAT Control |
| Network Status | Check network status | Network → Status |
| Network Details | Full network information | Network → Details |
| MAC Lookup | Find device by MAC | Device Lookup |
| SN Lookup | Find device by Serial # | Device Lookup |
| Export CSV | Download data | Available in most views |

## Default Credentials Location

The configuration page has these defaults:
- **Domain**: `https://api.tplinkcloud.com`
- **Cert**: `../certs/client.crt`
- **Key**: `../certs/client.key`

Adjust these in the web interface if your setup differs.

## Need Help?

- Full documentation: See `README.md`
- SDK documentation: See `../README.md`
- Architecture details: See `../CLAUDE.md`

---

**Ready to go?** Run `./run.sh` or `streamlit run app.py` and open the URL shown in your terminal (typically http://localhost:8765)!

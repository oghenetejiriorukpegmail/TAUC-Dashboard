# Port Management

This document explains the port management system implemented to avoid conflicts with Docker containers and other services.

## Problem Statement

Your system has multiple Docker containers using various ports:
- 7000, 7001, 7070, 7100 (Docker services)
- 6001, 6060, 6379, 6380 (Redis, etc.)
- 5004, 5432, 5433, 5500, 5501 (Databases)
- 8096, 8332, 8333 (Other services)
- 3000, 4000, 9002 (Web services)

## Solution Implemented

### 1. Smart Default Port Selection

**Changed from:** 8501 (Streamlit default)
**Changed to:** 8765 (verified available on your system)

This port is in a range (8765-8800) that doesn't conflict with your existing Docker containers.

### 2. Automatic Port Detection

Both launcher scripts now automatically find available ports:

#### Linux/Mac (`run.sh`)
```bash
# Checks ports 8765-8800
# Uses first available port
# Falls back gracefully if all ports busy
```

#### Windows (`run.bat`)
```batch
REM Checks ports 8765-8800
REM Uses first available port
REM Provides helpful error if none found
```

### 3. Port Helper Utility

Created `port_helper.py` for manual port management:

```bash
# Quick check - find available port
python3 port_helper.py

# Check specific port
python3 port_helper.py check 8765
# Output: ✓ Port 8765 is available

python3 port_helper.py check 7000
# Output: ✗ Port 7000 is in use

# Find port in custom range
python3 port_helper.py find 9000 9100

# List all used ports in range
python3 port_helper.py list 8000 9000
```

## Current Port Status on Your System

Tested and verified:
- ✅ **Port 8765** - Available (default choice)
- ✅ **Ports 8766-8800** - Available (fallback range)
- ❌ **Port 7000** - In use (Docker)
- ❌ **Port 6379** - In use (Redis)
- ❌ **Port 5432** - In use (PostgreSQL)

## Usage

### Quick Start (Recommended)
```bash
./run.sh    # Automatically finds and uses available port
```

### Manual Port Selection
```bash
# Use specific port
streamlit run app.py --server.port=9000

# Or set in .streamlit/config.toml
[server]
port = 9000
```

### Check Before Running
```bash
# Find out which port will be used
python3 port_helper.py

# Verify a specific port is free
python3 port_helper.py check 8765
```

## Port Range Strategy

**Primary Range:** 8765-8800 (36 ports)
- Chosen to avoid common Docker port ranges
- Far enough from your existing services
- Enough ports for multiple instances if needed

**Fallback Strategy:**
1. Try port 8765 (default)
2. If busy, try 8766, 8767, etc.
3. Continue up to 8800
4. If all busy, show helpful error with manual port suggestion

## Configuration Files Updated

1. **`.streamlit/config.toml`**
   - Changed default port from 8501 → 8765

2. **`run.sh`**
   - Added port checking logic
   - Auto-increments if port busy
   - Shows selected port in terminal

3. **`run.bat`**
   - Windows equivalent port checking
   - Same logic as bash script

4. **`port_helper.py`**
   - New utility for port management
   - Cross-platform (Windows/Linux/Mac)
   - Multiple checking strategies

## Troubleshooting

### All ports in range are busy
```bash
# Use custom port
streamlit run app.py --server.port=9500

# Or find available port in different range
python3 port_helper.py find 9500 9600
```

### Docker container starts after dashboard
If a new Docker container wants port 8765:
- Dashboard is already running → Docker will fail (as expected)
- Or, stop dashboard and restart (it will find next available port)

### Multiple dashboard instances
```bash
# First instance: will use 8765
./run.sh

# Second instance: will use 8766
./run.sh

# Third instance: will use 8767
./run.sh
```

## Testing

Verified on your system:
```bash
$ python3 port_helper.py check 8765
✓ Port 8765 is available

$ python3 port_helper.py check 7000
✗ Port 7000 is in use
```

## Summary

✅ **No manual port configuration needed**
✅ **Automatically avoids Docker container ports**
✅ **Graceful fallback to next available port**
✅ **Clear terminal output showing selected port**
✅ **Helper utility for troubleshooting**

The dashboard will now safely run alongside your Docker containers without any port conflicts!

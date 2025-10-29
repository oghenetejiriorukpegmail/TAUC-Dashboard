# Troubleshooting Guide

## Common Errors and Solutions

### Error: "Access token is required for OAuth 2.0 authentication"

**Symptom:**
```
Failed to fetch NAT-locked inventory: API call failed: Access token is required
for OAuth 2.0 authentication
```

**Root Cause:**
The access token is not present in the session when trying to make API calls.

**Solutions:**

#### 1. Check Session State (Quick Check)
1. Go to Home page
2. Expand "🔍 Debug Info (Session State)"
3. Check if "Access Token" shows a value or "None"

**If Access Token is None:**

#### 2. Re-authenticate
1. Click "Logout" in sidebar
2. Re-enter your credentials
3. Click "Authenticate with OAuth 2.0"
4. Look for: "Access token: xxx... (saved in session)"
5. If you see this, authentication worked!

#### 3. Verify SDK Installation
The authentication fixes must be applied:
```bash
cd /home/oghenetejiri/Documents/Tplink/TAUC/1.8.3/python-sdk
pip install -e .
```

Then restart the dashboard:
```bash
cd streamlit_app
./run.sh
```

#### 4. Check Browser Console
- Open browser developer tools (F12)
- Check Console tab for errors
- Try refreshing the page (F5)

#### 5. Clear Browser Cache
Sometimes Streamlit caches old session state:
- Hard refresh: Ctrl+Shift+R (Linux/Windows) or Cmd+Shift+R (Mac)
- Or clear browser cache completely

---

### Error: "X-Authorization header info is empty (Code: -70411)"

**This error should be fixed!** If you still see it:

1. **Reinstall SDK with fixes:**
```bash
cd /home/oghenetejiri/Documents/Tplink/TAUC/1.8.3/python-sdk
pip install -e .
```

2. **Restart Streamlit:**
```bash
# Kill existing dashboard
pkill -f "streamlit run"

# Restart
cd streamlit_app
./run.sh
```

3. **Verify the fix was applied:**
```python
python3 -c "
from tauc_openapi.execute.auth_manager import AuthManager
import inspect
source = inspect.getsource(AuthManager._attach_oauth_auth)
if 'X-Authorization' in source:
    print('✓ Fix applied: Using X-Authorization header')
else:
    print('✗ Fix NOT applied: Still using wrong header')
"
```

---

### Error: "Authentication succeeded but no access token was returned"

**Symptom:**
After clicking "Authenticate", you see success message but API says "Check API response"

**Possible Causes:**
1. API returned success but empty access_token field
2. Response format doesn't match expected structure

**Debug Steps:**

1. **Check the JSON response shown:**
The error message displays the API response. Look for:
- `error_code`: Should be 0 for success
- `result`: Should contain access_token

2. **Verify API endpoint:**
Ensure you're using correct domain:
```
https://api.tplinkcloud.com
```
Not:
- http:// (wrong protocol)
- Custom domain without https://

3. **Check credentials:**
- Client ID: Should be from TP-Link
- Client Secret: Should be from TP-Link
- These are NOT the same as your login username/password

---

### Error: "Certificate verify failed"

**Full Error:**
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Solutions:**

1. **Use absolute paths:**
```python
# Wrong
cert_path = "certs/client.crt"

# Correct
cert_path = "/home/oghenetejiri/Documents/Tplink/TAUC/1.8.3/python-sdk/certs/client.crt"
```

2. **Check certificates exist:**
```bash
ls -la /home/oghenetejiri/Documents/Tplink/TAUC/1.8.3/python-sdk/certs/
# Should show:
# client.crt
# client.key
```

3. **Verify certificate permissions:**
```bash
chmod 644 /path/to/certs/client.crt
chmod 600 /path/to/certs/client.key
```

---

### Error: "Invalid client credentials (Code: -70001)"

**Solutions:**

1. **Double-check credentials:**
- Are you using OAuth credentials (client_id/client_secret)?
- Or AK/SK credentials (access_key/secret_key)?
- Don't mix them up!

2. **Verify with TP-Link:**
Contact TP-Link support to verify your credentials are:
- Active
- Have correct permissions
- Not expired

3. **Check for typos:**
- Copy-paste credentials instead of typing
- Watch for extra spaces before/after

---

### Port Already in Use

**Symptom:**
```
Port 8765 is in use, trying next port...
```

This is **not an error** - the launcher automatically finds the next available port!

**If you want to use a specific port:**
```bash
streamlit run app.py --server.port=9000
```

---

## Debug Workflow

Follow this systematic approach:

### Step 1: Check Installation
```bash
cd /home/oghenetejiri/Documents/Tplink/TAUC/1.8.3/python-sdk
pip install -e .
```

### Step 2: Verify Imports
```python
python3 -c "from tauc_openapi import ApiClient; print('✓ SDK imports OK')"
```

### Step 3: Check Certificates
```bash
ls -la certs/
# Should show client.crt and client.key
```

### Step 4: Launch Dashboard
```bash
cd streamlit_app
./run.sh
```

### Step 5: Check Session State
1. Open http://localhost:8765 (or shown port)
2. Authenticate
3. Go to Home → Expand "Debug Info"
4. Verify access token is present

### Step 6: Test API Call
Try a simple operation first (like viewing inventory)

---

## Getting Help

### Information to Provide

When reporting issues, include:

1. **Error message:** Full text
2. **Session state:** From Debug Info panel
3. **Authentication type:** OAuth or AK/SK
4. **SDK installation:** Output of `pip show tauc-openapi`
5. **Browser:** Chrome, Firefox, etc.

### Useful Commands

```bash
# Check SDK version
pip show tauc-openapi

# Check port usage
python3 port_helper.py list 8000 9000

# Verify certificates
openssl x509 -in certs/client.crt -text -noout

# Check Python version
python3 --version

# Check Streamlit version
streamlit --version
```

---

## Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| Access token required | Logout → Re-authenticate |
| -70411 error | Reinstall SDK: `pip install -e .` |
| No access token returned | Check credentials and domain |
| Certificate error | Use absolute paths |
| Invalid credentials | Verify with TP-Link |
| Port conflict | Use `./run.sh` (auto-finds port) |
| Session state lost | Clear cache, re-authenticate |

---

## Windows-Specific Issues

### Issue: run.bat doesn't execute

**Symptom:**
```cmd
'run.bat' is not recognized as an internal or external command
```

**Solutions:**
1. **Make sure you're in the correct directory:**
   ```cmd
   cd streamlit_app
   dir run.bat
   ```

2. **Run with explicit path:**
   ```cmd
   .\run.bat
   ```
   Or:
   ```cmd
   call run.bat
   ```

3. **Check file exists:**
   ```cmd
   dir *.bat
   ```

### Issue: Python not found on Windows

**Symptom:**
```cmd
'python' is not recognized as an internal or external command
```

**Solutions:**
1. **Use `py` launcher instead:**
   ```cmd
   py -m pip install -r requirements.txt
   py -m streamlit run app.py
   ```

2. **Add Python to PATH:**
   - Open "Environment Variables" in System Properties
   - Add Python installation directory to PATH
   - Restart Command Prompt

3. **Use full path to Python:**
   ```cmd
   C:\Python310\python.exe -m pip install -r requirements.txt
   ```

### Issue: Permission denied on Windows

**Symptom:**
```cmd
PermissionError: [WinError 5] Access is denied
```

**Solutions:**
1. **Run Command Prompt as Administrator:**
   - Right-click Command Prompt
   - Select "Run as administrator"

2. **Use --user flag for pip:**
   ```cmd
   pip install --user -r requirements.txt
   ```

3. **Close other programs:**
   - Close any programs using the files
   - Close other Python processes
   - Try again

### Issue: Port already in use on Windows

**Symptom:**
```cmd
OSError: [WinError 10048] Only one usage of each socket address is normally permitted
```

**Solutions:**
1. **Use run.bat (finds available port automatically):**
   ```cmd
   run.bat
   ```

2. **Find process using port:**
   ```cmd
   netstat -ano | findstr :8765
   taskkill /PID <process_id> /F
   ```

3. **Use different port:**
   ```cmd
   streamlit run app.py --server.port=9000
   ```

### Issue: Certificate paths on Windows

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: '../certs/client.crt'
```

**Solutions:**
1. **Use absolute Windows paths:**
   ```
   C:\Users\YourName\Documents\TAUC\certs\client.crt
   C:\Users\YourName\Documents\TAUC\certs\client.key
   ```

2. **Use forward slashes (works on Windows):**
   ```
   C:/Users/YourName/Documents/TAUC/certs/client.crt
   ```

3. **Use raw strings in Python (avoid backslash issues):**
   ```python
   r"C:\Users\YourName\Documents\TAUC\certs\client.crt"
   ```

### Issue: Virtual environment on Windows

**Creating venv:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Activating venv:**
```cmd
# Command Prompt
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1

# If PowerShell execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Line endings on Windows (Git)

**Symptom:**
Run scripts have wrong line endings after cloning on Windows.

**Solution:**
```cmd
# Configure Git to handle line endings
git config --global core.autocrlf true

# Re-clone or reset files
git rm --cached -r .
git reset --hard
```

### Windows Quick Commands Reference

```cmd
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list

# Check if Streamlit installed
pip show streamlit

# Check if TAUC SDK installed
python -c "import tauc_openapi; print('SDK installed')"

# Find Python executable
where python

# Check available ports
netstat -ano | findstr LISTEN

# Kill process by PID
taskkill /PID <pid> /F
```

---

## Still Having Issues?

1. Check `README.md` for platform-specific installation guides
2. Check `ARCHITECTURE.md` for system design details
3. File an issue with:
   - Operating System and version (e.g., Windows 11, Linux Ubuntu 22.04)
   - Python version (`python --version`)
   - Full error message
   - Steps to reproduce
   - Debug Info output
   - SDK version

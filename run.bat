@echo off
REM TAUC Dashboard Launch Script for Windows

echo ===================================
echo TAUC Device Management Dashboard
echo ===================================
echo.

REM Check if streamlit is installed
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo Error: Streamlit is not installed
    echo Please run: pip install -r requirements.txt
    exit /b 1
)

REM Check if TAUC SDK is installed
python -c "import tauc_openapi" >nul 2>&1
if errorlevel 1 (
    echo Warning: TAUC SDK not found
    echo Installing SDK from parent directory...
    pip install -e ..
    if errorlevel 1 (
        echo Error: Failed to install TAUC SDK
        exit /b 1
    )
)

REM Find available port starting from 8765
set PORT=8765
set MAX_PORT=8800

echo Checking for available port...

:check_port_loop
netstat -an | findstr ":%PORT% " >nul 2>&1
if not errorlevel 1 (
    echo Port %PORT% is in use, trying next port...
    set /a PORT+=1
    if %PORT% gtr %MAX_PORT% (
        echo Error: No available ports found in range 8765-%MAX_PORT%
        echo Please specify a port manually: streamlit run app.py --server.port=XXXX
        exit /b 1
    )
    goto check_port_loop
)

echo Using port: %PORT%
echo Starting dashboard...
echo Access the dashboard at: http://localhost:%PORT%
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run streamlit with the selected port
streamlit run app.py --server.port=%PORT%

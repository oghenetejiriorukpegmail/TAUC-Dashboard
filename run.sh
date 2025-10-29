#!/bin/bash

# TAUC Dashboard Launch Script

echo "==================================="
echo "TAUC Device Management Dashboard"
echo "==================================="
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Error: Streamlit is not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if TAUC SDK is available (bundled with dashboard)
python -c "import tauc_openapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: TAUC SDK not found"
    echo "The SDK should be in the tauc_openapi/ directory"
    echo "Please ensure you have the complete repository"
    exit 1
fi

# Function to check if port is available
check_port() {
    local port=$1
    if command -v netstat &> /dev/null; then
        netstat -tuln 2>/dev/null | grep -q ":$port "
    elif command -v ss &> /dev/null; then
        ss -tuln 2>/dev/null | grep -q ":$port "
    else
        # Fallback: try to bind to the port
        (echo >/dev/tcp/localhost/$port) 2>/dev/null
    fi
    return $?
}

# Find available port starting from 8765
PORT=8765
MAX_PORT=8800

echo "Checking for available port..."
while check_port $PORT; do
    echo "Port $PORT is in use, trying next port..."
    PORT=$((PORT + 1))
    if [ $PORT -gt $MAX_PORT ]; then
        echo "Error: No available ports found in range 8765-$MAX_PORT"
        echo "Please specify a port manually: streamlit run app.py --server.port=XXXX"
        exit 1
    fi
done

echo "Using port: $PORT"
echo "Starting dashboard..."
echo "Access the dashboard at: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit with the selected port
streamlit run app.py --server.port=$PORT

#!/usr/bin/env python3
"""
Port availability helper for TAUC Dashboard.

This utility helps find available ports and checks for conflicts.
"""

import socket
import sys
from typing import Optional


def is_port_available(port: int) -> bool:
    """
    Check if a port is available.

    Args:
        port: Port number to check

    Returns:
        True if port is available, False if in use
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        return True
    except OSError:
        return False


def find_available_port(start_port: int = 8765, max_port: int = 8800) -> Optional[int]:
    """
    Find the first available port in a range.

    Args:
        start_port: Starting port number (default: 8765)
        max_port: Maximum port number to check (default: 8800)

    Returns:
        Available port number, or None if no ports available
    """
    for port in range(start_port, max_port + 1):
        if is_port_available(port):
            return port
    return None


def list_used_ports(start_port: int = 8000, end_port: int = 9000) -> list:
    """
    List all ports in use within a range.

    Args:
        start_port: Starting port number
        end_port: Ending port number

    Returns:
        List of ports that are in use
    """
    used_ports = []
    for port in range(start_port, end_port + 1):
        if not is_port_available(port):
            used_ports.append(port)
    return used_ports


def main():
    """Main CLI interface."""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "check":
            # Check specific port
            if len(sys.argv) < 3:
                print("Usage: python port_helper.py check <port>")
                sys.exit(1)

            port = int(sys.argv[2])
            if is_port_available(port):
                print(f"✓ Port {port} is available")
                sys.exit(0)
            else:
                print(f"✗ Port {port} is in use")
                sys.exit(1)

        elif command == "find":
            # Find available port
            start = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
            max_p = int(sys.argv[3]) if len(sys.argv) > 3 else 8800

            port = find_available_port(start, max_p)
            if port:
                print(f"✓ Available port found: {port}")
                print(f"\nTo use this port, run:")
                print(f"  streamlit run app.py --server.port={port}")
                sys.exit(0)
            else:
                print(f"✗ No available ports in range {start}-{max_p}")
                sys.exit(1)

        elif command == "list":
            # List used ports
            start = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
            end = int(sys.argv[3]) if len(sys.argv) > 3 else 9000

            print(f"Scanning ports {start}-{end}...")
            used = list_used_ports(start, end)

            if used:
                print(f"\n✗ Ports in use ({len(used)}):")
                for port in used:
                    print(f"  - {port}")
            else:
                print(f"\n✓ No ports in use in range {start}-{end}")
            sys.exit(0)

        else:
            print(f"Unknown command: {command}")
            print_usage()
            sys.exit(1)
    else:
        # Default: find available port
        port = find_available_port()
        if port:
            print(f"Recommended port: {port}")
            print(f"\nRun dashboard with:")
            print(f"  streamlit run app.py --server.port={port}")
            print(f"\nOr simply run:")
            print(f"  ./run.sh    (Linux/Mac)")
            print(f"  run.bat     (Windows)")
        else:
            print("No available ports found in range 8765-8800")
            sys.exit(1)


def print_usage():
    """Print usage information."""
    print("""
TAUC Dashboard Port Helper

Usage:
  python port_helper.py                    Find available port (8765-8800)
  python port_helper.py check <port>       Check if specific port is available
  python port_helper.py find [start] [max] Find available port in range
  python port_helper.py list [start] [end] List used ports in range

Examples:
  python port_helper.py                    # Find available port
  python port_helper.py check 8765         # Check if 8765 is available
  python port_helper.py find 9000 9100     # Find port between 9000-9100
  python port_helper.py list 8000 9000     # List used ports 8000-9000
""")


if __name__ == "__main__":
    main()

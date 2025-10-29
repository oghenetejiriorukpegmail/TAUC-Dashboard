"""
Shared utilities for TAUC Streamlit Dashboard.

This package contains reusable components to reduce code duplication
and ensure consistency across all pages.
"""

from .ui_components import (
    display_api_response,
    display_export_buttons,
    display_network_table,
    display_error_message,
    display_success_message
)

from .api_helpers import (
    make_api_call,
    get_network_by_name,
    validate_response,
    normalize_mac_address,
    validate_mac_address
)

__all__ = [
    # UI Components
    "display_api_response",
    "display_export_buttons",
    "display_network_table",
    "display_error_message",
    "display_success_message",
    # API Helpers
    "make_api_call",
    "get_network_by_name",
    "validate_response",
    "normalize_mac_address",
    "validate_mac_address",
]

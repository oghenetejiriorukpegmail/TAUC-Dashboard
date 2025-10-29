"""
API helper functions for the TAUC Streamlit Dashboard.

This module provides common patterns for making API calls and handling responses.
"""

import streamlit as st
from typing import Optional, Dict, List, Tuple, TypeVar, Type
from tauc_openapi.base.tauc_response import TAUCResponse

T = TypeVar('T', bound=TAUCResponse)


def make_api_call(request, response_class: Type[T], access_token: Optional[str] = None,
                  show_spinner: bool = True, spinner_text: str = "Processing...") -> Optional[T]:
    """
    Make an API call with consistent error handling.

    Args:
        request: TAUC request object
        response_class: Response class type
        access_token: Optional access token for OAuth
        show_spinner: Whether to show spinner during call
        spinner_text: Text to display in spinner

    Returns:
        Response object or None if error occurred
    """
    try:
        if not st.session_state.get('client'):
            st.error("Not authenticated. Please login first.")
            return None

        if show_spinner:
            with st.spinner(spinner_text):
                response = st.session_state.client.api_call(
                    request,
                    response_class,
                    access_token or st.session_state.get('access_token')
                )
        else:
            response = st.session_state.client.api_call(
                request,
                response_class,
                access_token or st.session_state.get('access_token')
            )

        return response

    except Exception as e:
        st.error(f"API call failed: {str(e)}")
        return None


def validate_response(response, success_message: Optional[str] = None,
                     show_errors: bool = True) -> bool:
    """
    Validate API response and display appropriate messages.

    Args:
        response: TAUC response object
        success_message: Optional message to show on success
        show_errors: Whether to display error messages

    Returns:
        True if response is successful, False otherwise
    """
    if not response:
        if show_errors:
            st.error("No response received from API")
        return False

    if response.is_success():
        if success_message:
            st.success(success_message)
        return True

    if show_errors:
        from .ui_components import display_error_message
        display_error_message(response.error_code, response.msg)

    return False


def get_network_by_name(network_name: str, page_size: str = "100",
                       case_sensitive: bool = False) -> Tuple[Optional[int], List[Dict]]:
    """
    Look up network ID by name using GetNetworkNameListV2.

    Args:
        network_name: Name of network to find
        page_size: Maximum results per query
        case_sensitive: Whether to match case-sensitively

    Returns:
        Tuple of (network_id, list of all matching networks)
        Returns (None, []) if not found or error
    """
    from tauc_openapi.models import GetNetworkNameListV2Request, GetNetworkNameListV2Response

    # Normalize search term
    search_name = network_name if case_sensitive else network_name.lower()

    # Query all network statuses
    statuses = ["ONLINE", "OFFLINE", "ABNORMAL", "INVENTORY", "NAT-LOCKED", "SUSPEND"]
    matched_networks = []

    for status in statuses:
        request = GetNetworkNameListV2Request(
            page="0",
            pageSize=page_size,
            networkStatus=status
        )

        response = make_api_call(
            request,
            GetNetworkNameListV2Response,
            show_spinner=False
        )

        if response and response.is_success() and response.result and response.result.data:
            for network in response.result.data:
                network_check_name = network.network_name if case_sensitive else (network.network_name or "").lower()

                if network_check_name == search_name:
                    matched_networks.append({
                        "id": network.id,
                        "name": network.network_name,
                        "status": status
                    })

    # Return first match and all matches
    if matched_networks:
        return matched_networks[0]["id"], matched_networks

    return None, []


def get_all_networks(page_size: str = "100",
                    status_filter: Optional[str] = None) -> Dict[int, Dict]:
    """
    Fetch all networks across all statuses.

    Args:
        page_size: Maximum results per status query
        status_filter: Optional status to filter by (ONLINE, OFFLINE, etc.)
                      If None, queries all statuses

    Returns:
        Dictionary of networks {id: {id, name, status}}
    """
    from tauc_openapi.models import GetNetworkNameListV2Request, GetNetworkNameListV2Response

    all_networks = {}

    # Determine which statuses to query
    if status_filter and status_filter != "ALL":
        statuses_to_query = [status_filter]
    else:
        statuses_to_query = ["ONLINE", "OFFLINE", "ABNORMAL", "INVENTORY", "NAT-LOCKED", "SUSPEND"]

    for status in statuses_to_query:
        request = GetNetworkNameListV2Request(
            page="0",
            pageSize=page_size,
            networkStatus=status
        )

        response = make_api_call(
            request,
            GetNetworkNameListV2Response,
            show_spinner=False
        )

        if response and response.is_success() and response.result and response.result.data:
            for network in response.result.data:
                if network.id:
                    all_networks[network.id] = {
                        "id": network.id,
                        "name": network.network_name or "Unnamed",
                        "status": status
                    }

    return all_networks


def batch_delete_with_progress(items: List[Dict], delete_function,
                               item_name_key: str = "name",
                               item_id_key: str = "id") -> Dict[str, any]:
    """
    Delete multiple items with progress tracking.

    Args:
        items: List of items to delete
        delete_function: Function to call for each delete (takes item dict)
        item_name_key: Key for item name in dict
        item_id_key: Key for item ID in dict

    Returns:
        Dictionary with success_count, failed_items list
    """
    success_count = 0
    failed_items = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, item in enumerate(items):
        item_name = item.get(item_name_key, f"Unknown (ID: {item.get(item_id_key)})")
        status_text.text(f"Processing {idx + 1}/{len(items)}: {item_name}")

        try:
            success = delete_function(item)
            if success:
                success_count += 1
            else:
                failed_items.append({
                    "item": item,
                    "error": "Delete function returned False"
                })
        except Exception as e:
            failed_items.append({
                "item": item,
                "error": str(e)
            })

        progress_bar.progress((idx + 1) / len(items))

    progress_bar.empty()
    status_text.empty()

    return {
        "success_count": success_count,
        "failed_items": failed_items,
        "total": len(items)
    }


def check_authentication() -> bool:
    """
    Check if user is authenticated.

    Returns:
        True if authenticated, False otherwise
    """
    if not st.session_state.get('authenticated'):
        st.warning("⚠️ Please authenticate first using the Configuration page")
        return False

    if not st.session_state.get('client'):
        st.error("⚠️ API client not initialized. Please re-authenticate.")
        return False

    return True


def normalize_mac_address(mac: str) -> str:
    """
    Normalize MAC address to standard format (uppercase, no separators).

    Accepts multiple formats:
    - AA:BB:CC:DD:EE:FF (colon separator)
    - AA-BB-CC-DD-EE-FF (dash separator)
    - AABBCCDDEEFF (no separator)
    - aabbccddeeff (lowercase)
    - aa:bb:cc:dd:ee:ff (lowercase with separator)

    Args:
        mac: MAC address in any common format

    Returns:
        Normalized MAC address (uppercase, no separators): AABBCCDDEEFF

    Example:
        >>> normalize_mac_address("aa:bb:cc:dd:ee:ff")
        'AABBCCDDEEFF'
        >>> normalize_mac_address("AA-BB-CC-DD-EE-FF")
        'AABBCCDDEEFF'
    """
    import re

    # Remove all non-alphanumeric characters (colons, dashes, dots, spaces)
    clean_mac = re.sub(r'[^0-9A-Fa-f]', '', mac)

    # Convert to uppercase
    return clean_mac.upper()


def validate_mac_address(mac: str, show_warning: bool = True) -> bool:
    """
    Validate MAC address format and length.

    Args:
        mac: MAC address to validate (can be in any format)
        show_warning: Whether to display Streamlit warning on invalid MAC

    Returns:
        True if MAC address is valid (12 hex characters), False otherwise
    """
    normalized = normalize_mac_address(mac)

    # Check if exactly 12 hexadecimal characters
    if len(normalized) != 12:
        if show_warning:
            st.warning(f"⚠️ MAC address should be 12 characters. Got {len(normalized)} characters after normalization.")
        return False

    # Check if all characters are valid hexadecimal
    import re
    if not re.match(r'^[0-9A-F]{12}$', normalized):
        if show_warning:
            st.warning("⚠️ MAC address contains invalid characters. Only 0-9 and A-F are allowed.")
        return False

    return True

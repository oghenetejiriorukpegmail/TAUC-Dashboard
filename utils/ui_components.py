"""
Reusable UI components for the TAUC Streamlit Dashboard.

This module provides consistent UI patterns across all pages.
"""

import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Optional, Any


def display_api_response(response, endpoint: str, show_full_data: bool = False):
    """
    Display API response in an expandable section with formatted JSON.

    Args:
        response: TAUC API response object
        endpoint: API endpoint URL
        show_full_data: If True, show full data array; if False, show count only
    """
    with st.expander("🔍 View Raw API Response"):
        st.code(f"Endpoint: {endpoint}", language="")

        # Build response JSON
        response_json = {
            "errorCode": response.error_code,
            "msg": response.msg,
        }

        if hasattr(response, 'result') and response.result:
            if hasattr(response.result, 'total'):
                # Paginated response
                result_data = {
                    "total": response.result.total,
                    "page": response.result.page,
                    "pageSize": response.result.page_size,
                }

                if show_full_data and hasattr(response.result, 'data') and response.result.data:
                    result_data["data"] = [vars(item) if hasattr(item, '__dict__') else item
                                          for item in response.result.data]
                else:
                    data_count = len(response.result.data) if hasattr(response.result, 'data') and response.result.data else 0
                    result_data["dataCount"] = data_count

                response_json["result"] = result_data
            else:
                # Non-paginated response
                response_json["result"] = vars(response.result) if hasattr(response.result, '__dict__') else response.result
        else:
            response_json["result"] = None

        st.json(response_json)


def display_export_buttons(data: List[Dict], filename_prefix: str, key_prefix: str = "export"):
    """
    Display export buttons for CSV and JSON formats.

    Args:
        data: List of dictionaries to export
        filename_prefix: Prefix for download filename
        key_prefix: Unique key prefix for buttons
    """
    if not data:
        st.info("No data to export")
        return

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        # CSV Export
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv",
            key=f"{key_prefix}_csv",
            use_container_width=True
        )

    with col2:
        # JSON Export
        json_data = json.dumps(data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"{filename_prefix}.json",
            mime="application/json",
            key=f"{key_prefix}_json",
            use_container_width=True
        )


def display_network_table(networks: Dict[int, Dict[str, Any]], show_actions: bool = False):
    """
    Display networks in a formatted table.

    Args:
        networks: Dictionary of networks {id: {id, name, status}}
        show_actions: If True, add action column (for future use)

    Returns:
        DataFrame of networks
    """
    if not networks:
        st.info("No networks found")
        return None

    # Convert to list and create DataFrame
    networks_list = list(networks.values())
    df_data = []

    for network in networks_list:
        row = {
            "Network ID": network.get("id"),
            "Network Name": network.get("name", "Unnamed"),
            "Status": network.get("status", "Unknown")
        }
        df_data.append(row)

    df = pd.DataFrame(df_data)

    # Display table
    st.dataframe(df, use_container_width=True, hide_index=True)

    return df


def display_error_message(error_code: int, message: str, show_common_solutions: bool = True):
    """
    Display error message with helpful context.

    Args:
        error_code: API error code
        message: Error message
        show_common_solutions: If True, show common solutions for known errors
    """
    st.error(f"Error {error_code}: {message}")

    if not show_common_solutions:
        return

    # Common error codes and solutions
    error_solutions = {
        -70325: {
            "title": "Parameter Validation Failed",
            "solutions": [
                "Ensure all required parameters are provided",
                "Check that parameter values are in the correct format",
                "Verify your account has access to this resource"
            ]
        },
        -70346: {
            "title": "Invalid Parameter",
            "solutions": [
                "Check that all parameter values are valid",
                "Ensure IDs exist in the system",
                "Verify parameter data types match API requirements"
            ]
        },
        -70435: {
            "title": "Access Token Expired",
            "solutions": [
                "Logout and re-authenticate to get a new token",
                "Token expires after a period of inactivity"
            ]
        },
        -40310: {
            "title": "Resource Not Found",
            "solutions": [
                "The requested resource does not exist",
                "Check that IDs are correct",
                "Verify you have access to this resource"
            ]
        }
    }

    if error_code in error_solutions:
        solution = error_solutions[error_code]
        with st.expander(f"💡 Common Solutions for Error {error_code}"):
            st.markdown(f"**{solution['title']}**")
            for sol in solution['solutions']:
                st.markdown(f"- {sol}")


def display_success_message(message: str, details: Optional[str] = None):
    """
    Display success message with optional details.

    Args:
        message: Success message
        details: Optional additional details
    """
    st.success(f"✅ {message}")

    if details:
        st.info(details)


def display_loading_spinner(text: str = "Processing..."):
    """
    Context manager for displaying a loading spinner.

    Usage:
        with display_loading_spinner("Fetching data..."):
            # Your code here
            pass
    """
    return st.spinner(text)


def display_metrics_row(metrics: List[Dict[str, Any]]):
    """
    Display a row of metrics using st.metric.

    Args:
        metrics: List of metric dicts with keys: label, value, delta (optional)

    Example:
        display_metrics_row([
            {"label": "Total Networks", "value": 42},
            {"label": "Online", "value": 38, "delta": "+2"},
            {"label": "Offline", "value": 4, "delta": "-1"}
        ])
    """
    if not metrics:
        return

    cols = st.columns(len(metrics))

    for idx, (col, metric) in enumerate(zip(cols, metrics)):
        with col:
            st.metric(
                label=metric.get("label", ""),
                value=metric.get("value", 0),
                delta=metric.get("delta")
            )


def display_info_card(title: str, content: str, icon: str = "ℹ️"):
    """
    Display an information card.

    Args:
        title: Card title
        content: Card content (supports markdown)
        icon: Icon to display
    """
    st.markdown(f"""
    <div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6; margin-bottom: 1rem;">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

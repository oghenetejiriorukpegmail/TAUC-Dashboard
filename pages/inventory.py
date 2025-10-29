"""Inventory management page."""

import streamlit as st
import json

import pandas as pd
from typing import List, Dict


def show():
    """Show inventory management page."""
    st.markdown(
        """
        <div class='tauc-hero'>
            <h1>Inventory Management</h1>
            <p>Audit online, offline, and NAT-locked networks with fast filters and exports.</p>
            <div style='display:flex;flex-wrap:wrap;gap:0.6rem;margin-top:1rem;'>
                <span class='tauc-chip'>All statuses</span>
                <span class='tauc-chip'>Real-time lookups</span>
                <span class='tauc-chip'>CSV / JSON export</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    # Tab layout
    tab1, tab2 = st.tabs(["All Inventory", "NAT-Locked Devices"])

    with tab1:
        show_all_inventory()

    with tab2:
        show_nat_locked_inventory()


def show_all_inventory():
    """Display all inventory using GetNetworkNameListV2."""
    st.subheader("All Registered Devices")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        page_size = st.selectbox("Page Size", [25, 50, 100], index=0, help="Maximum results per status")

    with col2:
        status_filter = st.selectbox(
            "Status Filter",
            ["ALL", "ONLINE", "OFFLINE", "ABNORMAL", "INVENTORY", "NAT-LOCKED", "SUSPEND"],
            index=0,
            help="Filter by network status"
        )

    with col3:
        st.write("")  # Spacing
        st.write("")  # Spacing
        fetch_button = st.button("Fetch Inventory", type="primary", key="fetch_all")

    if fetch_button:
        try:
            from tauc_openapi.models import GetNetworkNameListV2Request, GetNetworkNameListV2Response

            # Show endpoint info
            endpoint = "/v1/openapi/network-system-management/network-name-list"
            st.code(f"📡 Endpoint: GET {endpoint}", language="")

            # Determine which statuses to query
            if status_filter == "ALL":
                statuses_to_query = ["ONLINE", "OFFLINE", "ABNORMAL", "INVENTORY", "NAT-LOCKED", "SUSPEND"]
            else:
                statuses_to_query = [status_filter]

            all_networks = {}  # Use dict to avoid duplicates: {id: network_data}
            total_fetched = 0
            all_responses = []  # Store all API responses for display

            with st.spinner("Fetching all networks..."):
                for status in statuses_to_query:
                    st.caption(f"🔍 Querying {status} networks...")

                    # API uses zero-indexed pages (page=0 for first page)
                    request = GetNetworkNameListV2Request(
                        page="0",
                        pageSize=str(page_size),
                        networkStatus=status
                    )

                    response = st.session_state.client.api_call(
                        request,
                        GetNetworkNameListV2Response,
                        st.session_state.access_token
                    )

                    # Store response for viewing
                    all_responses.append({
                        "status": status,
                        "response": response
                    })

                    if response.is_success() and response.result and response.result.data:
                        count = len(response.result.data)
                        st.caption(f"  ✅ Found {count} {status} network(s)")
                        total_fetched += count

                        # Add to combined results (using ID as key to avoid duplicates)
                        for network in response.result.data:
                            if network.id:
                                all_networks[network.id] = {
                                    "id": network.id,
                                    "name": network.network_name or "Unnamed",
                                    "status": status
                                }
                    else:
                        st.caption(f"  ℹ️ No {status} networks")

                st.markdown(
                    f"""
                    <div class='tauc-status-card' style='text-align:left; margin-bottom:1.4rem;'>
                        <span style='font-size:0.9rem;'>📊 Total unique networks found</span>
                        <span style='font-size:1.4rem; font-weight:600;'>{len(all_networks)}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if all_networks:
                    display_network_list_results(all_networks, status_filter, endpoint, all_responses)
                else:
                    st.markdown(
                        """
                        <div class='tauc-notification'>
                            <div class='tauc-notification__title'>No networks found</div>
                            <div class='tauc-notification__meta'>Adjust your status filter or page size to broaden the search.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Still show API responses even if no data
                    with st.expander("🔍 View API Responses"):
                        for resp_data in all_responses:
                            st.markdown(f"**Status: {resp_data['status']}**")
                            st.code(f"Endpoint: GET {endpoint}?networkStatus={resp_data['status']}", language="")

                            response = resp_data['response']
                            st.json({
                                "errorCode": response.error_code,
                                "msg": response.msg,
                                "result": {
                                    "total": response.result.total if response.result else 0,
                                    "page": response.result.page if response.result else 0,
                                    "pageSize": response.result.page_size if response.result else 0,
                                    "data": []
                                }
                            })
                            st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Failed to fetch inventory: {str(e)}")


def show_nat_locked_inventory():
    """Display NAT-locked devices using GetNetworkNameListV2."""
    st.subheader("NAT-Locked (Suspended) Devices")

    st.markdown(
        """
        <div class='tauc-notification'>
            <div class='tauc-notification__title'>NAT-Locked overview</div>
            <div class='tauc-notification__meta'>Networks in this list are suspended until NAT access is restored.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        page_size = st.selectbox("Page Size", [25, 50, 100], index=0, key="nat_size", help="Maximum results to fetch")

    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        fetch_button = st.button("Fetch NAT-Locked", type="primary", key="fetch_nat")

    if fetch_button:
        try:
            from tauc_openapi.models import GetNetworkNameListV2Request, GetNetworkNameListV2Response

            # Show endpoint info
            endpoint = "/v1/openapi/network-system-management/network-name-list"
            st.code(f"📡 Endpoint: GET {endpoint}?networkStatus=NAT-LOCKED", language="")

            all_networks = {}
            all_responses = []

            with st.spinner("Fetching NAT-locked networks..."):
                # API uses zero-indexed pages (page=0 for first page)
                request = GetNetworkNameListV2Request(
                    page="0",
                    pageSize=str(page_size),
                    networkStatus="NAT-LOCKED"
                )

                response = st.session_state.client.api_call(
                    request,
                    GetNetworkNameListV2Response,
                    st.session_state.access_token
                )

                # Store response for viewing
                all_responses.append({
                    "status": "NAT-LOCKED",
                    "response": response
                })

                if response.is_success() and response.result and response.result.data:
                    count = len(response.result.data)
                    st.markdown(
                        f"""
                        <div class='tauc-status-card' style='text-align:left; margin-bottom:1.4rem;'>
                            <span style='font-size:0.9rem;'>✅ NAT-locked network count</span>
                            <span style='font-size:1.4rem; font-weight:600;'>{count}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Add to results
                    for network in response.result.data:
                        if network.id:
                            all_networks[network.id] = {
                                "id": network.id,
                                "name": network.network_name or "Unnamed",
                                "status": "NAT-LOCKED"
                            }

                    display_network_list_results(all_networks, "NAT-LOCKED", endpoint, all_responses)
                else:
                    st.markdown(
                        """
                        <div class='tauc-status-card' style='text-align:left; margin-bottom:1.4rem;'>
                            <span style='font-size:0.9rem;'>✅ No NAT-locked networks detected</span>
                            <span style='font-size:0.8rem; opacity:0.8;'>All networks are operating without suspension.</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Still show API response even if no data
                    with st.expander("🔍 View API Response"):
                        st.code(f"Endpoint: GET {endpoint}?networkStatus=NAT-LOCKED", language="")

                        st.json({
                            "errorCode": response.error_code,
                            "msg": response.msg,
                            "result": {
                                "total": response.result.total if response.result else 0,
                                "page": response.result.page if response.result else 0,
                                "pageSize": response.result.page_size if response.result else 0,
                                "data": []
                            }
                        })

        except Exception as e:
            st.error(f"Failed to fetch NAT-locked inventory: {str(e)}")


def display_network_list_results(all_networks: Dict, status_filter: str, endpoint: str, all_responses: List = None):
    """Display network list results in a formatted way."""

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    # Summary metrics styled as cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class='metric-card'>
                <p>Total Networks</p>
                <h3>{len(all_networks)}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class='metric-card'>
                <p>Status Filter</p>
                <h3 style='font-size:1.4rem;'>{status_filter}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    # Convert dict to list for display
    networks_list = list(all_networks.values())

    # Create DataFrame for display
    df_data = []
    for network in networks_list:
        df_data.append({
            "Network ID": network["id"],
            "Network Name": network["name"],
            "Status": network["status"]
        })

    df = pd.DataFrame(df_data)

    # Display table
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Export option
    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"tauc_networks_{status_filter.lower()}.csv",
            mime="text/csv",
            key=f"download_csv_{status_filter}"
        )

    with col2:
        import json

        json_data = json.dumps(networks_list, indent=2)
        st.download_button(
            label="⬇️ Download JSON",
            data=json_data,
            file_name=f"tauc_networks_{status_filter.lower()}.json",
            mime="application/json",
            key=f"download_json_{status_filter}"
        )

    # Show raw API responses
    if all_responses:
        st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
        with st.expander("🔍 View Raw API Responses"):
            for resp_data in all_responses:
                st.markdown(f"### Status: {resp_data['status']}")
                st.code(f"Endpoint: GET {endpoint}?page=0&pageSize=25&networkStatus={resp_data['status']}", language="")

                response = resp_data['response']

                # Build JSON response structure
                response_json = {
                    "errorCode": response.error_code,
                    "msg": response.msg,
                }

                if response.result:
                    result_data = {
                        "total": response.result.total,
                        "page": response.result.page,
                        "pageSize": response.result.page_size,
                        "data": []
                    }

                    if response.result.data:
                        for network in response.result.data:
                            result_data["data"].append({
                                "id": network.id,
                                "networkName": network.network_name
                            })

                    response_json["result"] = result_data
                else:
                    response_json["result"] = None

                st.json(response_json)
                st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

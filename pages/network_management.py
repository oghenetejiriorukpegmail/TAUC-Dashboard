"""Network management page."""

import streamlit as st
import json


def lookup_network_id(network_name: str) -> tuple[str, str]:
    """
    Look up network ID by network name.

    Returns:
        tuple: (network_id, error_message) - network_id is None if lookup failed
    """
    try:
        from tauc_openapi.models.network_system_management import GetNetworkIdRequest, GetNetworkIdResponse

        # Show endpoint being called
        endpoint = f"/v1/openapi/network-system-management/id?networkName={network_name}"
        st.caption(f"📡 Calling: GET {endpoint}")

        request = GetNetworkIdRequest(networkName=network_name)
        response = st.session_state.client.api_call(
            request,
            GetNetworkIdResponse,
            st.session_state.access_token
        )

        if response.is_success() and response.result:
            if len(response.result) == 0:
                return None, f"Network '{network_name}' not found"
            elif len(response.result) == 1:
                return str(response.result[0].id), None
            else:
                # Multiple matches, let user choose
                st.warning(f"Multiple networks match '{network_name}':")
                for item in response.result:
                    st.write(f"  - {item.networkName} (ID: {item.id})")
                return None, "Multiple matches found. Please be more specific."
        else:
            return None, f"Failed to look up network: {response.msg}"

    except Exception as e:
        return None, f"Error looking up network ID: {str(e)}"


def show():
    """Show network management page."""
    st.markdown(
        """
        <div class='tauc-hero'>
            <h1>Network Management</h1>
            <p>Control NAT state, inspect network diagnostics, and review device groups in one place.</p>
            <div style='display:flex;flex-wrap:wrap;gap:0.6rem;margin-top:1rem;'>
                <span class='tauc-chip'>NAT control</span>
                <span class='tauc-chip'>Status insights</span>
                <span class='tauc-chip'>Detailed metadata</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    # Tab layout
    tab1, tab2, tab3 = st.tabs(["NAT Control", "Network Status", "Network Details"])

    with tab1:
        show_nat_control()

    with tab2:
        show_network_status()

    with tab3:
        show_network_details()


def show_nat_control():
    """NAT lock/unlock control panel."""
    st.subheader("NAT Lock/Unlock Control")

    st.markdown(
        """
        <div class='tauc-notification'>
            <div class='tauc-notification__title'>How NAT locking works</div>
            <div class='tauc-notification__meta'>Locking suspends internet access until the network is unlocked again. Enter a network name and TAUC will resolve the ID automatically.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔒 Lock NAT")
        st.caption("Suspend a network by locking NAT")

        lock_network_name = st.text_input(
            "Network Name to Lock",
            key="lock_network_name",
            help="Enter the network name (will be looked up automatically)",
            placeholder="e.g., customer_1"
        )

        if st.button("Lock NAT", type="primary", key="lock_button"):
            if not lock_network_name:
                st.error("Please enter a network name")
            else:
                # Look up network ID
                with st.spinner(f"Looking up network '{lock_network_name}'..."):
                    network_id, error = lookup_network_id(lock_network_name)

                if error:
                    st.error(error)
                else:
                    st.success(f"✓ Found network ID: {network_id}")
                    lock_nat(network_id, lock_network_name)

    with col2:
        st.markdown("### 🔓 Unlock NAT")
        st.caption("Resume a suspended network")

        unlock_network_name = st.text_input(
            "Network Name to Unlock",
            key="unlock_network_name",
            help="Enter the network name (will be looked up automatically)",
            placeholder="e.g., customer_1"
        )

        if st.button("Unlock NAT", type="primary", key="unlock_button"):
            if not unlock_network_name:
                st.error("Please enter a network name")
            else:
                # Look up network ID
                with st.spinner(f"Looking up network '{unlock_network_name}'..."):
                    network_id, error = lookup_network_id(unlock_network_name)

                if error:
                    st.error(error)
                else:
                    st.success(f"✓ Found network ID: {network_id}")
                    unlock_nat(network_id, unlock_network_name)


def lock_nat(network_id: str, network_name: str):
    """Lock NAT for a network."""
    try:
        from tauc_openapi.models import NATLockMeshControllerRequest, NATLockMeshControllerResponse

        # Show endpoint
        endpoint = f"/v1/openapi/network-system-management/block/{network_id}"
        st.code(f"📡 Endpoint: POST {endpoint}", language="")

        with st.spinner(f"Locking NAT for '{network_name}' (ID: {network_id})..."):
            request = NATLockMeshControllerRequest(network_id=network_id)

            response = st.session_state.client.api_call(
                request,
                NATLockMeshControllerResponse,
                st.session_state.access_token
            )

            if response.is_success():
                st.success(f"✓ Successfully locked NAT for '{network_name}' (ID: {network_id})")

                # Show raw JSON response
                with st.expander("🔍 View Raw JSON Response"):
                    st.code(f"Endpoint: POST {endpoint}", language="")

                    # Get the actual raw JSON response from the API
                    raw_json = response.get_raw_json()
                    if raw_json:
                        st.json(raw_json)
                    else:
                        st.error("Raw JSON response not available")
            else:
                st.error(f"Failed to lock NAT: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error locking NAT: {str(e)}")


def unlock_nat(network_id: str, network_name: str):
    """Unlock NAT for a network."""
    try:
        from tauc_openapi.models import NATUnlockMeshControllerRequest, NATUnlockMeshControllerResponse

        # Show endpoint
        endpoint = f"/v1/openapi/network-system-management/unblock/{network_id}"
        st.code(f"📡 Endpoint: POST {endpoint}", language="")

        with st.spinner(f"Unlocking NAT for '{network_name}' (ID: {network_id})..."):
            request = NATUnlockMeshControllerRequest(network_id=network_id)

            response = st.session_state.client.api_call(
                request,
                NATUnlockMeshControllerResponse,
                st.session_state.access_token
            )

            if response.is_success():
                st.success(f"✓ Successfully unlocked NAT for '{network_name}' (ID: {network_id})")

                # Show raw JSON response
                with st.expander("🔍 View Raw JSON Response"):
                    st.code(f"Endpoint: POST {endpoint}", language="")

                    # Get the actual raw JSON response from the API
                    raw_json = response.get_raw_json()
                    if raw_json:
                        st.json(raw_json)
                    else:
                        st.error("Raw JSON response not available")
            else:
                st.error(f"Failed to unlock NAT: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error unlocking NAT: {str(e)}")


def show_network_status():
    """Show network status lookup."""
    st.subheader("Network Status Lookup")

    st.markdown("Check the current status of a network.")
    st.info("💡 Enter the network name (e.g., 'customer_1') - the system will look up the ID automatically.")

    network_name = st.text_input(
        "Network Name",
        key="status_network_name",
        help="Enter the network name to check status",
        placeholder="e.g., customer_1"
    )

    if st.button("Get Status", type="primary", key="status_button"):
        if not network_name:
            st.error("Please enter a network name")
        else:
            # Look up network ID
            with st.spinner(f"Looking up network '{network_name}'..."):
                network_id, error = lookup_network_id(network_name)

            if error:
                st.error(error)
            else:
                st.success(f"✓ Found network ID: {network_id}")
                get_network_status(network_id, network_name)


def get_network_status(network_id: str, network_name: str):
    """Get network status."""
    try:
        from tauc_openapi.models import GetNetworkStatusRequest, GetNetworkStatusResponse

        # Show endpoint
        endpoint = f"/v1/openapi/network-system-management/status/{network_id}"
        st.code(f"📡 Endpoint: GET {endpoint}", language="")

        with st.spinner(f"Fetching status for '{network_name}' (ID: {network_id})..."):
            request = GetNetworkStatusRequest(network_id=network_id)

            response = st.session_state.client.api_call(
                request,
                GetNetworkStatusResponse,
                st.session_state.access_token
            )

            if response.is_success():
                st.success(f"✓ Successfully retrieved status for '{network_name}' (ID: {network_id})")

                if response.result:
                    # Display status in a formatted way
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("#### Network Status")
                        if hasattr(response.result, 'status'):
                            # Map status to colors: green for online/active, red for offline/inactive, yellow for others
                            status_upper = response.result.status.upper() if response.result.status else ""
                            if status_upper in ["ONLINE", "ACTIVE", "UP"]:
                                status_color = "🟢"
                            elif status_upper in ["OFFLINE", "INACTIVE", "DOWN"]:
                                status_color = "🔴"
                            else:
                                status_color = "🟡"  # Unknown status
                            st.markdown(f"{status_color} **Status:** {response.result.status}")

                    with col2:
                        st.markdown("#### Additional Information")
                        # Display all available fields
                        result_dict = {}
                        for attr in dir(response.result):
                            if not attr.startswith('_') and not callable(getattr(response.result, attr)):
                                value = getattr(response.result, attr)
                                if value is not None:
                                    result_dict[attr] = value

                        if result_dict:
                            st.json(result_dict)

                    # Show raw JSON response
                    with st.expander("🔍 View Raw JSON Response"):
                        st.code(f"Endpoint: GET {endpoint}", language="")

                        # Get the actual raw JSON response from the API
                        raw_json = response.get_raw_json()
                        if raw_json:
                            st.json(raw_json)
                        else:
                            st.error("Raw JSON response not available")
                else:
                    st.info("No status information available")

            else:
                st.error(f"Failed to get status: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error getting status: {str(e)}")


def show_network_details():
    """Show network details lookup."""
    st.subheader("Network Details Lookup")

    st.markdown("Get comprehensive details about a network including all devices.")
    st.info("💡 Enter the network name (e.g., 'customer_1') - the system will look up the ID automatically.")

    network_name = st.text_input(
        "Network Name",
        key="details_network_name",
        help="Enter the network name to view details",
        placeholder="e.g., customer_1"
    )

    if st.button("Get Details", type="primary", key="details_button"):
        if not network_name:
            st.error("Please enter a network name")
        else:
            # Look up network ID
            with st.spinner(f"Looking up network '{network_name}'..."):
                network_id, error = lookup_network_id(network_name)

            if error:
                st.error(error)
            else:
                st.success(f"✓ Found network ID: {network_id}")
                get_network_details(network_id, network_name)


def get_network_details(network_id: str, network_name: str):
    """Get network details."""
    try:
        from tauc_openapi.models import GetNetworkDetailsRequest, GetNetworkDetailsResponse
        import pandas as pd

        # Show endpoint
        endpoint = f"/v1/openapi/network-system-management/details/{network_id}"
        st.code(f"📡 Endpoint: GET {endpoint}", language="")

        with st.spinner(f"Fetching details for '{network_name}' (ID: {network_id})..."):
            request = GetNetworkDetailsRequest(network_id=network_id)

            response = st.session_state.client.api_call(
                request,
                GetNetworkDetailsResponse,
                st.session_state.access_token
            )

            if response.is_success():
                st.success(f"✓ Successfully retrieved details for '{network_name}' (ID: {network_id})")

                if response.result and hasattr(response.result, 'network'):
                    network = response.result.network

                    # Network Information
                    st.markdown("### 🌐 Network Information")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if hasattr(network, 'network_name') and network.network_name:
                            st.metric("Network Name", network.network_name)

                    with col2:
                        if hasattr(network, 'network_id') and network.network_id:
                            st.metric("Network ID", network.network_id)

                    with col3:
                        if hasattr(network, 'address') and network.address:
                            st.metric("Address", network.address)

                    # Additional network info
                    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)

                    with col1:
                        if hasattr(network, 'create_time') and network.create_time:
                            st.text(f"📅 Created: {network.create_time}")

                        if hasattr(network, 'update_time') and network.update_time:
                            st.text(f"🔄 Updated: {network.update_time}")

                    with col2:
                        # Display any other network attributes
                        other_attrs = {}
                        for attr in dir(network):
                            if not attr.startswith('_') and attr not in ['network_name', 'network_id', 'address', 'create_time', 'update_time', 'mesh_unit_list'] and not callable(getattr(network, attr)):
                                value = getattr(network, attr)
                                if value is not None:
                                    other_attrs[attr] = value

                        if other_attrs:
                            st.json(other_attrs)

                    # Devices in network
                    if hasattr(network, 'mesh_unit_list') and network.mesh_unit_list:
                        st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
                        st.markdown("### 📱 Devices in Network")

                        devices_data = []
                        for unit in network.mesh_unit_list:
                            device_info = {
                                "Serial Number": unit.sn or "N/A",
                                "MAC Address": unit.mac or "N/A",
                            }

                            # Add all available fields
                            for attr in dir(unit):
                                if not attr.startswith('_') and attr not in ['sn', 'mac'] and not callable(getattr(unit, attr)):
                                    value = getattr(unit, attr)
                                    if value is not None:
                                        device_info[attr.replace('_', ' ').title()] = value

                            devices_data.append(device_info)

                        # Display as table
                        df = pd.DataFrame(devices_data)
                        st.dataframe(df, use_container_width=True)

                        # Export option
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Devices CSV",
                            data=csv,
                            file_name=f"network_{network_id}_devices.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No devices found in this network")

                    # Show raw JSON response
                    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
                    with st.expander("🔍 View Raw JSON Response"):
                        st.code(f"Endpoint: GET {endpoint}", language="")

                        # Get the actual raw JSON response from the API
                        raw_json = response.get_raw_json()
                        if raw_json:
                            st.json(raw_json)
                        else:
                            st.error("Raw JSON response not available")

                else:
                    st.info("No details available")

            else:
                st.error(f"Failed to get details: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error getting details: {str(e)}")

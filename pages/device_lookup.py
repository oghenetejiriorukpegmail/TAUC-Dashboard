"""Device information lookup page."""

import streamlit as st
from utils import normalize_mac_address, validate_mac_address


def show():
    """Show device lookup page."""
    st.markdown(
        """
        <div class='tauc-hero'>
            <h1>Device Lookup</h1>
            <p>Resolve device IDs and firmware details by pairing serial numbers with MAC addresses.</p>
            <div style='display:flex;flex-wrap:wrap;gap:0.6rem;margin-top:1rem;'>
                <span class='tauc-chip'>SN + MAC required</span>
                <span class='tauc-chip'>Normalized MAC input</span>
                <span class='tauc-chip'>Quick exports</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    lookup_device()


def lookup_device():
    """Lookup device by SN and MAC (both required)."""
    st.subheader("Device Lookup")

    st.markdown(
        """
        <div class='tauc-notification'>
            <div class='tauc-notification__title'>Provide both identifiers</div>
            <div class='tauc-notification__meta'>Supply the serial number and MAC address to guarantee a unique match. Check the Inventory or Network Details modules if you need the values.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        serial_number = st.text_input(
            "Serial Number (SN)",
            placeholder="22360N3001039",
            help="Device serial number (13 or 18 characters)"
        )

    with col2:
        mac_address = st.text_input(
            "MAC Address",
            placeholder="AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF or AABBCCDDEEFF",
            help="Device MAC address - accepts colon (:), dash (-), or no separator; uppercase or lowercase"
        )

    col_btn, col_space = st.columns([1, 3])
    with col_btn:
        search_button = st.button("Search Device", type="primary", use_container_width=True)

    if search_button:
        if not serial_number or not mac_address:
            st.error("⚠️ Both Serial Number AND MAC Address are required!")
        else:
            # Normalize MAC address (handles :, -, uppercase, lowercase)
            clean_mac = normalize_mac_address(mac_address)

            # Validate MAC address
            validate_mac_address(clean_mac, show_warning=True)

            # Validate serial number
            if len(serial_number) not in [13, 18]:
                st.warning(f"Serial number should be 13 or 18 characters. You entered {len(serial_number)} characters. Proceeding anyway...")

            # Search with both parameters
            search_device(sn=serial_number, mac=clean_mac)


def validate_mac(mac: str) -> bool:
    """Basic MAC address validation."""
    import re
    # Basic MAC address pattern (multiple formats)
    patterns = [
        r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',  # AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF
        r'^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})$',    # AABB.CCDD.EEFF
        r'^([0-9A-Fa-f]{12})$'                          # AABBCCDDEEFF
    ]

    for pattern in patterns:
        if re.match(pattern, mac):
            return True
    return False


def display_device_information(sn: str, mac: str, device_id: str, device_info_list: list, id_response, info_response, endpoint1: str, endpoint2: str):
    """Display detailed device information from both API calls."""
    import pandas as pd

    # Get the first device info (should only be one for a specific device ID)
    device_info = device_info_list[0] if device_info_list else None

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📋 Device Information")

    # Section 1: Search Criteria Used
    with st.expander("🔍 Search Criteria", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Serial Number (SN)", sn)
        with col2:
            st.metric("MAC Address", mac)

    # Section 2: Device Details
    if device_info:
        st.markdown("### 📱 Device Details")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Device Category", device_info.device_category or "N/A")

        with col2:
            # Show topology role with icon
            role = device_info.topo_role or "N/A"
            role_icon = "👑" if role == "MASTER" else "📡" if role == "SLAVE" else "⚪"
            st.metric("Topology Role", f"{role_icon} {role}")

        with col3:
            st.metric("Device Model", device_info.device_model or "N/A")

        with col4:
            st.metric("Firmware Version", device_info.fw_version or "N/A")

        # Additional info if available
        if device_info.imei:
            st.info(f"**IMEI:** {device_info.imei}")

        # Topology Role explanation
        with st.expander("ℹ️ What is Topology Role?"):
            st.markdown("""
            **Topology Role** indicates the device's function in the network:

            - **👑 MASTER**: The main device (FAP - Fat Access Point) of the network. This is the primary router/gateway.
            - **📡 SLAVE**: A satellite device that extends the network coverage (mesh node/repeater).
            - **⚪ INACTIVE**: The device hasn't been activated yet.
            """)

    # Section 3: Device ID
    st.markdown("### 🆔 Device Identifier")
    st.markdown(
        """
        <div class='tauc-notification'>
            <div class='tauc-notification__title'>Why the Device ID matters</div>
            <div class='tauc-notification__meta'>Use the returned device identifier for Wi-Fi configuration calls, firmware upgrades, status polling, and reboot/reset commands.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display Device ID prominently
    st.markdown(f"**Device ID:**")
    st.code(device_id, language=None)

    # Section 4: Device Summary Table
    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Device Summary")

    if device_info:
        device_summary = {
            "Property": [
                "Serial Number",
                "MAC Address",
                "Device Category",
                "Topology Role",
                "Device Model",
                "Firmware Version",
                "Device ID"
            ],
            "Value": [
                sn,
                mac,
                device_info.device_category or "N/A",
                device_info.topo_role or "N/A",
                device_info.device_model or "N/A",
                device_info.fw_version or "N/A",
                device_id[:50] + "..." if len(device_id) > 50 else device_id
            ]
        }
    else:
        device_summary = {
            "Property": ["Serial Number", "MAC Address", "Device ID"],
            "Value": [sn, mac, device_id[:50] + "..." if len(device_id) > 50 else device_id]
        }

    df = pd.DataFrame(device_summary)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Section 5: Export Options
    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 💾 Export")

    col1, col2, col3 = st.columns(3)

    with col1:
        # CSV Export
        if device_info:
            csv_data = f"Property,Value\nSerial Number,{sn}\nMAC Address,{mac}\nDevice Category,{device_info.device_category or 'N/A'}\nTopology Role,{device_info.topo_role or 'N/A'}\nDevice Model,{device_info.device_model or 'N/A'}\nFirmware Version,{device_info.fw_version or 'N/A'}\nDevice ID,{device_id}\n"
        else:
            csv_data = f"Property,Value\nSerial Number,{sn}\nMAC Address,{mac}\nDevice ID,{device_id}\n"

        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"device_{sn}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        # Text Export
        if device_info:
            text_data = f"""Device Information
{'='*50}

Serial Number: {sn}
MAC Address: {mac}
Device Category: {device_info.device_category or 'N/A'}
Topology Role: {device_info.topo_role or 'N/A'}
Device Model: {device_info.device_model or 'N/A'}
Firmware Version: {device_info.fw_version or 'N/A'}
Device ID: {device_id}
"""
        else:
            text_data = f"Device Information\n{'='*50}\n\nSerial Number: {sn}\nMAC Address: {mac}\nDevice ID: {device_id}\n"

        st.download_button(
            label="📄 Download TXT",
            data=text_data,
            file_name=f"device_{sn}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col3:
        if st.button("🔄 New Search", use_container_width=True):
            st.rerun()

    # Section 6: Raw API Responses
    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🔍 Raw API Responses")

    with st.expander("📡 Step 1: Get Device ID Response"):
        st.code(f"Endpoint: GET {endpoint1}", language="")

        # Get the actual raw JSON response from the API
        raw_json1 = id_response.get_raw_json()
        if raw_json1:
            st.json(raw_json1)
        else:
            st.error("Raw JSON response not available")

    with st.expander("📡 Step 2: Get Device Info Response"):
        st.code(f"Endpoint: GET {endpoint2}", language="")

        # Get the actual raw JSON response from the API
        raw_json2 = info_response.get_raw_json()
        if raw_json2:
            st.json(raw_json2)
        else:
            st.error("Raw JSON response not available")


def search_device(sn: str, mac: str):
    """Search for device by SN and MAC (both required)."""
    try:
        from tauc_openapi.models import GetDeviceIdRequest, GetDeviceIdResponse, GetDeviceInfoRequest, GetDeviceInfoResponse

        # Step 1: Get Device ID
        endpoint1 = f"/v1/openapi/device-information/device-id?sn={sn}&mac={mac}"
        st.code(f"📡 Step 1: GET {endpoint1}", language="")

        with st.spinner(f"Step 1: Looking up device ID for SN: {sn} and MAC: {mac}..."):
            # Build request with BOTH parameters (API requires both)
            request = GetDeviceIdRequest(sn=sn, mac=mac)

            response = st.session_state.client.api_call(
                request,
                GetDeviceIdResponse,
                st.session_state.access_token
            )

            if response.is_success():
                if response.result and response.result.device_id:
                    device_id = response.result.device_id
                    st.success(f"✅ Step 1 Complete: Device ID obtained!")

                    # Step 2: Get Detailed Device Information
                    endpoint2 = f"/v1/openapi/device-information/device-info/{device_id}"
                    st.code(f"📡 Step 2: GET {endpoint2}", language="")

                    with st.spinner(f"Step 2: Fetching detailed device information..."):
                        info_request = GetDeviceInfoRequest(device_id=device_id)

                        info_response = st.session_state.client.api_call(
                            info_request,
                            GetDeviceInfoResponse,
                            st.session_state.access_token
                        )

                        if info_response.is_success() and info_response.result:
                            st.success(f"✅ Step 2 Complete: Device details retrieved!")

                            # Display both responses
                            display_device_information(
                                sn=sn,
                                mac=mac,
                                device_id=device_id,
                                device_info_list=info_response.result,
                                id_response=response,
                                info_response=info_response,
                                endpoint1=endpoint1,
                                endpoint2=endpoint2
                            )
                        else:
                            st.warning("Device ID obtained, but detailed information could not be retrieved.")
                            st.error(f"Error: {info_response.msg} (Code: {info_response.error_code})")

                            # Show raw response for debugging
                            with st.expander("🔍 View Error Response"):
                                raw_json = info_response.get_raw_json()
                                if raw_json:
                                    st.json(raw_json)

                else:
                    st.warning("Device found but no Device ID returned")

            else:
                st.error(f"Device not found: {response.msg} (Code: {response.error_code})")

                # Helpful error messages
                if response.error_code == -70346:
                    st.info("""
                    💡 **Error -70346: Invalid Parameter**

                    This error usually means:
                    - The serial number format is incorrect
                    - The device is not registered in the TAUC system yet
                    - The serial number doesn't match any device in your account

                    **Suggestions:**
                    1. Check that you copied the exact serial number from Inventory or Network Details
                    2. Make sure the device is registered and showing up in your inventory
                    3. Try searching by MAC address instead
                    4. Verify the device belongs to your account
                    """)
                elif response.error_code == -1:
                    st.info("💡 **Tip:** Make sure the MAC address or Serial Number is correct and the device is registered in the system.")

                # Show raw response for debugging
                with st.expander("🔍 View Error Response Details"):
                    raw_json = response.get_raw_json()
                    if raw_json:
                        st.json(raw_json)
                    else:
                        st.json({
                            "errorCode": response.error_code,
                            "msg": response.msg,
                            "httpCode": response.http_code
                        })

    except Exception as e:
        st.error(f"Search error: {str(e)}")

        # Debug information
        with st.expander("Debug Information"):
            st.code(str(e))
            st.text(f"Serial Number: {sn}")
            st.text(f"MAC Address: {mac}")


# Additional utility: Bulk lookup
def show_bulk_lookup():
    """Show bulk lookup interface (future enhancement)."""
    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
    st.subheader("🔄 Bulk Lookup (Coming Soon)")

    st.markdown(
        """
        <div class='tauc-notification'>
            <div class='tauc-notification__title'>Bulk lookup preview</div>
            <div class='tauc-notification__meta'>Upcoming support to upload CSVs with SN/MAC pairs for batch resolution. The control is disabled until the API is finalised.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=['csv'],
        disabled=True,
        help="This feature is not yet implemented"
    )


# Call bulk lookup at the end of main show function if needed

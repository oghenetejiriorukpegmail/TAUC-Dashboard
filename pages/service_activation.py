"""Service Activation page - Network provisioning and batch operations."""

import streamlit as st
import json
import time
from utils import normalize_mac_address, validate_mac_address


def show():
    """Show service activation page."""
    st.title("🌐 Service Activation")

    st.markdown("""
    Provision and manage networks in bulk. Available operations:
    - **Add Network**: Create a single network with full configuration
    - **Batch Add Networks**: Provision multiple networks in one operation
    - **Check Batch Results**: Monitor batch operation status
    - **Delete Networks**: Remove networks from the system
    """)

    # Tab layout
    tab1, tab2, tab3, tab4 = st.tabs(["Add Network", "Batch Add Networks", "Batch Results", "Delete Networks"])

    with tab1:
        show_add_network()

    with tab2:
        show_batch_add_networks()

    with tab3:
        show_batch_results()

    with tab4:
        show_delete_networks()


def show_add_network():
    """Add a single network."""
    st.subheader("Add Network")

    st.info("""
    Create a new network with device serial number(s), MAC address(es), and wireless pre-configuration.
    """)

    # Initialize mesh unit count in session state
    if 'mesh_unit_count' not in st.session_state:
        st.session_state.mesh_unit_count = 1

    with st.form("add_network_form"):
        st.markdown("### Network Information")

        network_name = st.text_input(
            "Network Name *",
            help="Unique identifier for the network",
            placeholder="e.g., Customer Network Alpha"
        )

        st.markdown("---")
        st.markdown("### Device Information")

        # Add/Remove mesh unit buttons (inside Device Information section, outside form using columns)
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            add_device = st.form_submit_button("➕ Add Device", help="Add another device", type="primary")
            if add_device:
                st.session_state.mesh_unit_count += 1
                st.rerun()
        with col2:
            remove_device = st.form_submit_button("➖ Remove", help="Remove last device", type="secondary", disabled=st.session_state.mesh_unit_count <= 1)
            if remove_device and st.session_state.mesh_unit_count > 1:
                st.session_state.mesh_unit_count -= 1
                st.rerun()
        with col3:
            st.caption(f"Total devices: {st.session_state.mesh_unit_count}")

        st.markdown("---")

        # Collect mesh units
        mesh_unit_inputs = []
        for i in range(st.session_state.mesh_unit_count):
            st.markdown(f"**Device {i + 1}**")
            col1, col2 = st.columns(2)

            with col1:
                sn = st.text_input(
                    f"Serial Number {i + 1} *",
                    key=f"sn_{i}",
                    help="Device serial number",
                    placeholder="e.g., SN123456"
                )

            with col2:
                mac = st.text_input(
                    f"MAC Address {i + 1} *",
                    key=f"mac_{i}",
                    help="Device MAC address - accepts colon (:), dash (-), or no separator; uppercase or lowercase",
                    placeholder="e.g., AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF"
                )

            mesh_unit_inputs.append({"sn": sn, "mac": mac})

            if i < st.session_state.mesh_unit_count - 1:
                st.markdown("---")

        st.markdown("---")
        st.markdown("### Pre-Configuration (Optional)")

        with st.expander("Wireless Configuration"):
            operation_mode = st.selectbox(
                "Operation Mode *",
                options=["Router", "AP", "DSL", "Mobile"],
                help="Required when configuring wireless settings. DSL and Mobile are only for Deco devices."
            )

            # Internet configuration (required for Router mode)
            if operation_mode == "Router":
                st.markdown("**Internet Configuration** (Required for Router mode)")
                internet_type = st.selectbox(
                    "Connection Type",
                    options=["dynamic_ip", "static_ip", "pppoe", "pptp", "l2tp", "none"],
                    index=0,  # Default to dynamic_ip
                    help="Type of internet connection"
                )
            else:
                internet_type = None

            st.markdown("**Wireless Settings**")
            ssid = st.text_input("SSID", placeholder="MyNetwork-5G")
            password = st.text_input("Password", type="password")
            enable_band_steering = st.checkbox("Enable Band Steering", value=True)

        submitted = st.form_submit_button("Create Network", type="primary")

        if submitted:
            if not network_name:
                st.error("Network Name is required!")
                return

            # Validate and normalize all mesh units
            mesh_units = []
            for i, unit in enumerate(mesh_unit_inputs):
                if not unit["sn"] or not unit["mac"]:
                    st.error(f"Device {i + 1}: Both Serial Number and MAC Address are required!")
                    return

                # Normalize MAC address
                normalized_mac = normalize_mac_address(unit["mac"])
                validate_mac_address(normalized_mac, show_warning=True)

                mesh_units.append({"sn": unit["sn"], "mac": normalized_mac})

            # Build pre-config
            pre_config = None
            if ssid or password:
                pre_config = {
                    "operation_mode": operation_mode,
                    "wireless": {
                        "ssid": ssid,
                        "password": password,
                        "enable_band_steering": enable_band_steering
                    }
                }

                # Add internet config if Router mode
                if operation_mode == "Router" and internet_type:
                    pre_config["internet"] = {
                        "type": internet_type
                    }

            # Call API
            add_network(
                network_name=network_name,
                mesh_units=mesh_units,
                pre_config=pre_config
            )


def add_network(network_name, mesh_units, pre_config):
    """Execute add network API call."""
    try:
        from tauc_openapi.models import AddNetworkRequest, AddNetworkResponse
        from tauc_openapi.models.service_activation_services import (
            MeshUnit, PreConfig, PreConfigWireless, PreConfigInternet
        )

        # Show endpoint
        endpoint = "/v1/openapi/service-activation-services/network"
        st.caption(f"📡 Calling: POST {endpoint}")

        # Build mesh units
        mesh_unit_list = None
        if mesh_units:
            mesh_unit_list = [MeshUnit(sn=m["sn"], mac=m["mac"]) for m in mesh_units]

        # Build pre-config
        pre_config_obj = None
        if pre_config and pre_config.get("wireless"):
            w = pre_config["wireless"]

            # Build internet config if present
            internet_obj = None
            if pre_config.get("internet"):
                i = pre_config["internet"]
                internet_obj = PreConfigInternet(
                    type=i.get("type")
                )

            pre_config_obj = PreConfig(
                operation_mode=pre_config.get("operation_mode"),
                wireless=PreConfigWireless(
                    ssid=w.get("ssid"),
                    password=w.get("password"),
                    enable_band_steering=w.get("enable_band_steering")
                ),
                internet=internet_obj
            )

        # Create request
        request = AddNetworkRequest(
            network_name=network_name,
            mesh_unit_list=mesh_unit_list,
            pre_config=pre_config_obj
        )

        # Execute
        with st.spinner("Creating network..."):
            response = st.session_state.client.api_call(
                request,
                AddNetworkResponse,
                st.session_state.access_token
            )

        if response.is_success():
            st.success(f"✓ Network created successfully! Network ID: {response.result.id}")

            if response.result.failed_mesh_unit_list:
                st.warning("Device registration failed:")
                for unit in response.result.failed_mesh_unit_list:
                    st.error(f"  - SN: {unit.sn}, MAC: {unit.mac} - Error: {unit.error}")
            else:
                st.info("Device registered successfully!")

            # Show response
            with st.expander("📄 API Response"):
                st.json({
                    "error_code": response.error_code,
                    "message": response.msg,
                    "network_id": response.result.id,
                    "failed_units": len(response.result.failed_mesh_unit_list) if response.result.failed_mesh_unit_list else 0
                })
        else:
            st.error(f"Failed to create network: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error creating network: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


def show_batch_add_networks():
    """Batch add multiple networks."""
    st.subheader("Batch Add Networks")

    st.info("""
    Submit multiple networks in a single batch operation. The operation is asynchronous
    and returns a task ID that you can use to check the results.
    """)

    st.markdown("### Upload Networks")

    # Sample JSON template
    sample_json = [
        {
            "network_name": "Network Alpha",
            "username": "user1",
            "email": "user1@example.com",
            "phone_number": "+1234567890",
            "address": "123 Main St",
            "mesh_unit_list": [
                {"sn": "SN001", "mac": "AA:BB:CC:DD:EE:01"}
            ],
            "tags": [
                {"name": "location", "value": "building-a"}
            ]
        },
        {
            "network_name": "Network Beta",
            "username": "user2",
            "email": "user2@example.com",
            "mesh_unit_list": [
                {"sn": "SN002", "mac": "AA:BB:CC:DD:EE:02"}
            ]
        }
    ]

    with st.expander("📋 JSON Template (Click to Expand)"):
        st.json(sample_json)
        st.caption("Copy this template and modify it with your network data")

    networks_json = st.text_area(
        "Networks JSON (array of network objects)",
        help="Paste JSON array of networks to create",
        height=300,
        placeholder=json.dumps(sample_json, indent=2)
    )

    if st.button("Submit Batch Request", type="primary"):
        if not networks_json:
            st.error("Please enter networks JSON!")
            return

        # Parse JSON
        try:
            networks_data = json.loads(networks_json)
            if not isinstance(networks_data, list):
                st.error("JSON must be an array of network objects!")
                return

            st.info(f"Parsed {len(networks_data)} networks")

            # Call API
            batch_add_networks(networks_data)

        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {str(e)}")


def batch_add_networks(networks_data):
    """Execute batch add networks API call."""
    try:
        from tauc_openapi.models import BatchAddingNetworksRequest, BatchAddingNetworksResponse
        from tauc_openapi.models.service_activation_services import SingleNetwork, MeshUnit, Tag

        # Show endpoint
        endpoint = "/v1/openapi/service-activation-services/networks"
        st.caption(f"📡 Calling: POST {endpoint}")

        # Build networks list
        networks = []
        for net_data in networks_data:
            # Parse mesh units with normalized MAC addresses
            mesh_units = None
            if net_data.get("mesh_unit_list"):
                mesh_units = [
                    MeshUnit(sn=m["sn"], mac=normalize_mac_address(m["mac"]))
                    for m in net_data["mesh_unit_list"]
                ]

            # Parse tags
            tags = None
            if net_data.get("tags"):
                tags = [
                    Tag(name=t["name"], value=t["value"])
                    for t in net_data["tags"]
                ]

            networks.append(SingleNetwork(
                network_name=net_data.get("network_name"),
                username=net_data.get("username"),
                email=net_data.get("email"),
                phone_number=net_data.get("phone_number"),
                address=net_data.get("address"),
                mesh_unit_list=mesh_units,
                tags=tags
            ))

        # Create request
        request = BatchAddingNetworksRequest(networks_list=networks)

        # Execute
        with st.spinner("Submitting batch request..."):
            response = st.session_state.client.api_call(
                request,
                BatchAddingNetworksResponse,
                st.session_state.access_token
            )

        if response.is_success():
            task_id = response.result.task_id
            st.success(f"✓ Batch request submitted successfully!")
            st.info(f"Task ID: `{task_id}`")
            st.caption("Copy this Task ID and use it in the 'Batch Results' tab to check status")

            # Store in session state for easy access
            if 'batch_task_ids' not in st.session_state:
                st.session_state.batch_task_ids = []
            st.session_state.batch_task_ids.insert(0, task_id)

            # Show response
            with st.expander("📄 API Response"):
                st.json({
                    "error_code": response.error_code,
                    "message": response.msg,
                    "task_id": task_id
                })
        else:
            st.error(f"Failed to submit batch request: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error submitting batch request: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


def show_batch_results():
    """Check batch operation results."""
    st.subheader("Check Batch Results")

    st.info("""
    Poll the status of a batch network addition operation using the task ID
    returned from the batch request.
    """)

    # Show recent task IDs if available
    if 'batch_task_ids' in st.session_state and st.session_state.batch_task_ids:
        st.markdown("### Recent Task IDs")
        for i, tid in enumerate(st.session_state.batch_task_ids[:5]):
            if st.button(f"Load: {tid}", key=f"load_task_{i}"):
                st.session_state.selected_task_id = tid
                st.rerun()

        st.markdown("---")

    task_id = st.text_input(
        "Task ID",
        value=st.session_state.get('selected_task_id', ''),
        help="Enter the task ID from the batch request",
        placeholder="e.g., abc123def456"
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("Check Status", type="primary"):
            if not task_id:
                st.error("Please enter a task ID!")
            else:
                get_batch_result(task_id)

    with col2:
        if st.button("Auto-Poll (10 attempts)", type="secondary"):
            if not task_id:
                st.error("Please enter a task ID!")
            else:
                auto_poll_batch_result(task_id)


def get_batch_result(task_id):
    """Get batch operation result."""
    try:
        from tauc_openapi.models import GetBatchAddingResultRequest, GetBatchAddingResultResponse

        # Show endpoint
        endpoint = f"/v1/openapi/service-activation-services/networks-result/{task_id}"
        st.caption(f"📡 Calling: GET {endpoint}")

        request = GetBatchAddingResultRequest(task_id=task_id)

        with st.spinner("Fetching batch results..."):
            response = st.session_state.client.api_call(
                request,
                GetBatchAddingResultResponse,
                st.session_state.access_token
            )

        if response.is_success() and response.result:
            st.success(f"✓ Batch operation completed! Processed {len(response.result)} networks")

            # Display results
            for idx, network in enumerate(response.result, 1):
                with st.expander(f"Network {idx}: {network.network_name}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Username:**", network.username)
                        st.write("**Email:**", network.email or "N/A")
                        st.write("**Phone:**", network.phone_number or "N/A")

                    with col2:
                        st.write("**Address:**", network.address or "N/A")

                        if network.mesh_unit_list:
                            st.write(f"**Mesh Units:** {len(network.mesh_unit_list)}")
                            for unit in network.mesh_unit_list:
                                if unit.error_info:
                                    st.error(f"❌ SN: {unit.sn} - {unit.error_info}")
                                else:
                                    st.success(f"✓ SN: {unit.sn}, MAC: {unit.mac}")

        elif response.is_success() and not response.result:
            st.warning("Task is still processing or has no results yet. Try again in a few seconds.")

        else:
            st.error(f"Failed to get results: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error fetching batch results: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


def auto_poll_batch_result(task_id):
    """Auto-poll batch result with retries."""
    max_attempts = 10
    attempt = 0

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        from tauc_openapi.models import GetBatchAddingResultRequest, GetBatchAddingResultResponse

        while attempt < max_attempts:
            attempt += 1
            progress_bar.progress(attempt / max_attempts)
            status_text.text(f"Attempt {attempt}/{max_attempts}...")

            request = GetBatchAddingResultRequest(task_id=task_id)
            response = st.session_state.client.api_call(
                request,
                GetBatchAddingResultResponse,
                st.session_state.access_token
            )

            if response.is_success() and response.result:
                status_text.empty()
                progress_bar.empty()
                st.success(f"✓ Results available after {attempt} attempts!")
                get_batch_result(task_id)  # Display results
                return

            if attempt < max_attempts:
                time.sleep(3)

        status_text.empty()
        progress_bar.empty()
        st.warning(f"No results after {max_attempts} attempts. Task may still be processing.")

    except Exception as e:
        status_text.empty()
        progress_bar.empty()
        st.error(f"Error during auto-poll: {str(e)}")


def show_delete_networks():
    """Delete multiple networks."""
    st.subheader("Delete Networks")

    st.info("""
    Remove networks from the system by entering their network names.
    The system will look up the network IDs automatically.
    """)

    # Initialize network count in session state
    if 'delete_network_count' not in st.session_state:
        st.session_state.delete_network_count = 1

    with st.form("delete_networks_form"):
        st.markdown("### Networks to Delete")

        # Add/Remove network buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            add_network = st.form_submit_button("➕ Add Network", help="Add another network")
            if add_network:
                st.session_state.delete_network_count += 1
                st.rerun()
        with col2:
            remove_network = st.form_submit_button("➖ Remove", help="Remove last network", disabled=st.session_state.delete_network_count <= 1)
            if remove_network and st.session_state.delete_network_count > 1:
                st.session_state.delete_network_count -= 1
                st.rerun()
        with col3:
            st.caption(f"Total networks: {st.session_state.delete_network_count}")

        st.markdown("---")

        # Collect network names
        network_names = []
        for i in range(st.session_state.delete_network_count):
            st.markdown(f"**Network {i + 1}**")

            network_name = st.text_input(
                f"Network Name {i + 1} *",
                key=f"delete_network_name_{i}",
                help="Network name to delete",
                placeholder="e.g., OrukpeHomeNetwork"
            )

            network_names.append(network_name)

            if i < st.session_state.delete_network_count - 1:
                st.markdown("---")

        st.markdown("---")
        st.warning("⚠️ **Warning**: This action will permanently delete the specified networks. This cannot be undone.")

        submitted = st.form_submit_button("Lookup & Delete Networks", type="primary")

        if submitted:
            # Validate all network names are provided
            for i, name in enumerate(network_names):
                if not name or not name.strip():
                    st.error(f"Network {i + 1}: Network Name is required!")
                    return

            # Filter out empty names
            valid_names = [name.strip() for name in network_names if name.strip()]

            # Lookup network IDs
            lookup_and_delete_networks(valid_names)


def lookup_and_delete_networks(network_names):
    """Lookup network IDs by name and delete networks."""
    try:
        from tauc_openapi.models import GetNetworkNameListV2Request, GetNetworkNameListV2Response

        # Fetch all networks using GetNetworkNameListV2
        # Strategy: Try without networkStatus first, if that fails due to validation,
        # try with each known status value
        all_networks = {}  # Use dict to avoid duplicates: {id: network}

        with st.spinner("Fetching all networks..."):
            # API uses zero-indexed pages (page=0 for first page)
            # Try each known status value to get all networks
            network_statuses = ["ONLINE", "OFFLINE", "ABNORMAL", "INVENTORY"]

            for status in network_statuses:
                request = GetNetworkNameListV2Request(page="0", pageSize="100", networkStatus=status)

                # Debug: Show exact request parameters
                st.caption(f"📡 Fetching {status} networks...")
                st.caption(f"   URL: {request.get_url()}")
                st.caption(f"   Params: page={request.page}, pageSize={request.pageSize}, networkStatus={request.networkStatus}")

                response = st.session_state.client.api_call(
                    request,
                    GetNetworkNameListV2Response,
                    st.session_state.access_token
                )

                # Debug: Show response
                st.caption(f"   Response: error_code={response.error_code}, msg={response.msg}")
                if response.result:
                    st.caption(f"   Result: total={response.result.total}, page={response.result.page}, data_count={len(response.result.data) if response.result.data else 0}")

                if response.is_success() and response.result and response.result.data:
                    st.caption(f"✓ Found {len(response.result.data)} {status} networks")
                    for network in response.result.data:
                        if network.id:
                            all_networks[network.id] = network
                elif not response.is_success() and response.error_code != -70301:
                    # -70301 means "Network does not exist" which is OK (no networks with that status)
                    # Other errors should be reported
                    st.warning(f"Error fetching {status} networks: {response.msg} (Code: {response.error_code})")

        if not all_networks:
            st.error("No networks found in the system!")
            return

        st.success(f"📊 Total networks found: {len(all_networks)}")

        # Build name to ID mapping (case-insensitive)
        name_to_network = {}
        for network in all_networks.values():
            if network.network_name:
                name_to_network[network.network_name.lower()] = {
                    "id": network.id,
                    "name": network.network_name
                }

        # Match requested names to networks
        matched_networks = []
        not_found = []

        for requested_name in network_names:
            requested_lower = requested_name.lower()
            if requested_lower in name_to_network:
                matched_networks.append(name_to_network[requested_lower])
            else:
                not_found.append(requested_name)

        # Show results
        if not_found:
            st.error("The following networks were not found:")
            for name in not_found:
                st.error(f"  - {name}")

        if not matched_networks:
            st.warning("No matching networks found. Please check the network names and try again.")
            return

        # Show matched networks
        st.success(f"Found {len(matched_networks)} matching network(s):")
        for network in matched_networks:
            st.info(f"  - {network['name']} (ID: {network['id']})")

        # Proceed with deletion immediately
        network_ids = [n["id"] for n in matched_networks]
        delete_networks(network_ids, matched_networks)

    except Exception as e:
        st.error(f"Error during network lookup: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


def delete_networks(network_ids, network_details):
    """Execute delete networks API call."""
    try:
        from tauc_openapi.models import DeleteNetworkRequest, DeleteNetworkResponse

        # Create a mapping of ID to name for display
        id_to_name = {n["id"]: n["name"] for n in network_details}

        # Delete each network individually
        success_count = 0
        failed_deletions = []

        for network_id in network_ids:
            network_name = id_to_name.get(network_id, f"Unknown (ID: {network_id})")

            # Show progress
            st.caption(f"🗑️ Deleting: {network_name} (ID: {network_id})...")

            # Create request
            request = DeleteNetworkRequest(networkId=network_id)

            # Execute
            response = st.session_state.client.api_call(
                request,
                DeleteNetworkResponse,
                st.session_state.access_token
            )

            # Handle response
            if response.is_success():
                success_count += 1
                st.caption(f"   ✅ Deleted successfully")
            else:
                failed_deletions.append({
                    "name": network_name,
                    "id": network_id,
                    "error": f"{response.msg} (Code: {response.error_code})"
                })
                st.caption(f"   ❌ Failed: {response.msg}")

        # Show summary
        if success_count > 0:
            st.success(f"✅ Successfully deleted {success_count} of {len(network_ids)} network(s)!")

        if failed_deletions:
            st.error(f"❌ Failed to delete {len(failed_deletions)} network(s):")
            for failure in failed_deletions:
                st.write(f"- {failure['name']}: {failure['error']}")

    except Exception as e:
        st.error(f"Error deleting networks: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

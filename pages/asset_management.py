"""Asset Management page - Device asset operations."""

import streamlit as st
import json
import time
from utils import normalize_mac_address, validate_mac_address


def show():
    """Show asset management page."""
    st.title("📦 Asset Management")

    st.markdown("""
    Manage device assets in your inventory. Available operations:
    - **Add Asset**: Register a single device asset
    - **Batch Add Assets**: Register multiple assets in one operation
    - **Check Batch Results**: Monitor batch operation status
    - **Delete Asset**: Remove a device asset from inventory
    """)

    # Tab layout
    tab1, tab2, tab3, tab4 = st.tabs(["Add Asset", "Batch Add Assets", "Batch Results", "Delete Asset"])

    with tab1:
        show_add_asset()

    with tab2:
        show_batch_add_assets()

    with tab3:
        show_batch_results()

    with tab4:
        show_delete_asset()


def show_add_asset():
    """Add a single asset."""
    st.subheader("Add Asset")

    st.info("""
    Register a single device asset in the inventory by providing its serial number and MAC address.
    """)

    with st.form("add_asset_form"):
        col1, col2 = st.columns(2)

        with col1:
            sn = st.text_input(
                "Serial Number (SN) *",
                help="Device serial number",
                placeholder="e.g., DEVICE-SN-123456"
            )

        with col2:
            mac = st.text_input(
                "MAC Address *",
                help="Device MAC address - accepts colon (:), dash (-), or no separator; uppercase or lowercase",
                placeholder="e.g., AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF"
            )

        st.markdown("---")

        submitted = st.form_submit_button("Add Asset", type="primary")

        if submitted:
            if not sn or not mac:
                st.error("Both Serial Number and MAC Address are required!")
                return

            # Normalize MAC address
            normalized_mac = normalize_mac_address(mac)
            validate_mac_address(normalized_mac, show_warning=True)

            # Call API
            add_asset(sn, normalized_mac)


def add_asset(sn, mac):
    """Execute add asset API call."""
    try:
        from tauc_openapi.models import AddAssetRequest, AddAssetResponse

        # Show endpoint
        endpoint = "/v1/openapi/device-asset-management/device"
        st.caption(f"📡 Calling: POST {endpoint}")

        # Create request
        request = AddAssetRequest(sn=sn, mac=mac)

        # Execute
        with st.spinner("Adding asset..."):
            response = st.session_state.client.api_call(
                request,
                AddAssetResponse,
                st.session_state.access_token
            )

        if response.is_success():
            if response.result and response.result.failed_assets:
                st.warning("Asset operation completed with errors:")
                for asset in response.result.failed_assets:
                    st.error(f"""
                    **Failed Asset:**
                    - SN: {asset.sn}
                    - MAC: {asset.mac}
                    - Error Code: {asset.error_code}
                    - Message: {asset.message}
                    """)
            else:
                st.success("✓ Asset added successfully!")

            # Show response
            with st.expander("📄 API Response"):
                st.json({
                    "error_code": response.error_code,
                    "message": response.msg,
                    "failed_assets": len(response.result.failed_assets) if response.result and response.result.failed_assets else 0
                })
        else:
            st.error(f"Failed to add asset: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error adding asset: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


def show_batch_add_assets():
    """Batch add multiple assets."""
    st.subheader("Batch Add Assets")

    st.info("""
    Submit multiple assets in a single batch operation. The operation is asynchronous
    and returns a task ID that you can use to check the results.
    """)

    st.markdown("### Upload Assets")

    # Method selection
    method = st.radio(
        "Input Method",
        ["JSON Format", "CSV/Text Format"],
        horizontal=True
    )

    if method == "JSON Format":
        # Sample JSON template
        sample_json = [
            {"sn": "DEVICE-SN-001", "mac": "AA:BB:CC:DD:EE:01"},
            {"sn": "DEVICE-SN-002", "mac": "AA:BB:CC:DD:EE:02"},
            {"sn": "DEVICE-SN-003", "mac": "AA:BB:CC:DD:EE:03"},
            {"sn": "DEVICE-SN-004", "mac": "AA:BB:CC:DD:EE:04"},
            {"sn": "DEVICE-SN-005", "mac": "AA:BB:CC:DD:EE:05"}
        ]

        with st.expander("📋 JSON Template (Click to Expand)"):
            st.json(sample_json)
            st.caption("Copy this template and modify it with your asset data")

        assets_json = st.text_area(
            "Assets JSON (array of asset objects)",
            help="Paste JSON array of assets to add",
            height=300,
            placeholder=json.dumps(sample_json, indent=2)
        )

        if st.button("Submit Batch Request", type="primary", key="json_submit"):
            if not assets_json:
                st.error("Please enter assets JSON!")
                return

            # Parse JSON
            try:
                assets_data = json.loads(assets_json)
                if not isinstance(assets_data, list):
                    st.error("JSON must be an array of asset objects!")
                    return

                st.info(f"Parsed {len(assets_data)} assets")

                # Call API
                batch_add_assets(assets_data)

            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {str(e)}")

    else:  # CSV/Text Format
        st.markdown("**Format:** One asset per line in format: `SN,MAC`")

        sample_csv = """DEVICE-SN-001,AA:BB:CC:DD:EE:01
DEVICE-SN-002,AA:BB:CC:DD:EE:02
DEVICE-SN-003,AA:BB:CC:DD:EE:03
DEVICE-SN-004,AA:BB:CC:DD:EE:04
DEVICE-SN-005,AA:BB:CC:DD:EE:05"""

        with st.expander("📋 CSV Example"):
            st.code(sample_csv)

        assets_text = st.text_area(
            "Assets (one per line: SN,MAC)",
            help="Enter assets in CSV format",
            height=300,
            placeholder=sample_csv
        )

        if st.button("Submit Batch Request", type="primary", key="csv_submit"):
            if not assets_text:
                st.error("Please enter asset data!")
                return

            # Parse CSV
            assets_data = []
            for line in assets_text.strip().split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) == 2:
                        assets_data.append({"sn": parts[0], "mac": parts[1]})
                    else:
                        st.warning(f"Skipping invalid line: {line}")

            if not assets_data:
                st.error("No valid assets found!")
                return

            st.info(f"Parsed {len(assets_data)} assets")

            # Call API
            batch_add_assets(assets_data)


def batch_add_assets(assets_data):
    """Execute batch add assets API call."""
    try:
        from tauc_openapi.models import BatchAddingAssetsRequest, BatchAddingAssetsResponse
        from tauc_openapi.models.device_asset_management import Asset

        # Show endpoint
        endpoint = "/v1/openapi/device-asset-management/devices"
        st.caption(f"📡 Calling: POST {endpoint}")

        # Build assets list with normalized MAC addresses
        assets = [Asset(sn=a["sn"], mac=normalize_mac_address(a["mac"])) for a in assets_data]

        # Create request
        request = BatchAddingAssetsRequest(assets=assets)

        # Execute
        with st.spinner("Submitting batch request..."):
            response = st.session_state.client.api_call(
                request,
                BatchAddingAssetsResponse,
                st.session_state.access_token
            )

        if response.is_success():
            task_id = response.result.task_id
            new_task = response.result.new_task

            st.success(f"✓ Batch request submitted successfully!")
            st.info(f"Task ID: `{task_id}`")

            if new_task is not None:
                if new_task:
                    st.caption("✓ New task created")
                else:
                    st.caption("⚠️ Merged with existing task")

            st.caption("Copy this Task ID and use it in the 'Batch Results' tab to check status")

            # Store in session state for easy access
            if 'asset_task_ids' not in st.session_state:
                st.session_state.asset_task_ids = []
            st.session_state.asset_task_ids.insert(0, task_id)

            # Show response
            with st.expander("📄 API Response"):
                st.json({
                    "error_code": response.error_code,
                    "message": response.msg,
                    "task_id": task_id,
                    "new_task": new_task
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
    Poll the status of a batch asset addition operation using the task ID
    returned from the batch request.
    """)

    # Show recent task IDs if available
    if 'asset_task_ids' in st.session_state and st.session_state.asset_task_ids:
        st.markdown("### Recent Task IDs")
        for i, tid in enumerate(st.session_state.asset_task_ids[:5]):
            if st.button(f"Load: {tid}", key=f"load_asset_task_{i}"):
                st.session_state.selected_asset_task_id = tid
                st.rerun()

        st.markdown("---")

    task_id = st.text_input(
        "Task ID",
        value=st.session_state.get('selected_asset_task_id', ''),
        help="Enter the task ID from the batch request",
        placeholder="e.g., abc123def456"
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("Check Status", type="primary"):
            if not task_id:
                st.error("Please enter a task ID!")
            else:
                get_batch_task_result(task_id)

    with col2:
        if st.button("Auto-Poll (10 attempts)", type="secondary"):
            if not task_id:
                st.error("Please enter a task ID!")
            else:
                auto_poll_batch_result(task_id)


def get_batch_task_result(task_id):
    """Get batch task result."""
    try:
        from tauc_openapi.models import GetBatchTaskResultRequest, GetBatchTaskResultResponse

        # Show endpoint
        endpoint = f"/v1/openapi/device-asset-management/devices/devices-result/{task_id}"
        st.caption(f"📡 Calling: GET {endpoint}")

        request = GetBatchTaskResultRequest(task_id=task_id)

        with st.spinner("Fetching batch results..."):
            response = st.session_state.client.api_call(
                request,
                GetBatchTaskResultResponse,
                st.session_state.access_token
            )

        if response.is_success():
            if response.result and response.result.failed_assets:
                st.warning(f"⚠️ Batch operation completed with {len(response.result.failed_assets)} failed assets")

                # Display failed assets
                for idx, asset in enumerate(response.result.failed_assets, 1):
                    with st.expander(f"Failed Asset {idx}: {asset.sn}"):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.write("**Serial Number:**", asset.sn)
                            st.write("**MAC Address:**", asset.mac)

                        with col2:
                            st.error(f"**Error Code:** {asset.error_code}")
                            st.error(f"**Message:** {asset.message}")

            else:
                st.success("✓ All assets added successfully! No failures reported.")

            # Show response
            with st.expander("📄 API Response"):
                st.json({
                    "error_code": response.error_code,
                    "message": response.msg,
                    "failed_count": len(response.result.failed_assets) if response.result and response.result.failed_assets else 0
                })

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
        from tauc_openapi.models import GetBatchTaskResultRequest, GetBatchTaskResultResponse

        while attempt < max_attempts:
            attempt += 1
            progress_bar.progress(attempt / max_attempts)
            status_text.text(f"Attempt {attempt}/{max_attempts}...")

            request = GetBatchTaskResultRequest(task_id=task_id)
            response = st.session_state.client.api_call(
                request,
                GetBatchTaskResultResponse,
                st.session_state.access_token
            )

            if response.is_success():
                status_text.empty()
                progress_bar.empty()
                st.success(f"✓ Results available after {attempt} attempts!")
                get_batch_task_result(task_id)  # Display results
                return

            if attempt < max_attempts:
                time.sleep(3)

        status_text.empty()
        progress_bar.empty()
        st.warning(f"No conclusive results after {max_attempts} attempts. Task may still be processing.")

    except Exception as e:
        status_text.empty()
        progress_bar.empty()
        st.error(f"Error during auto-poll: {str(e)}")


def show_delete_asset():
    """Delete a single asset."""
    st.subheader("Delete Asset")

    st.info("""
    Remove a single device asset from the inventory by providing its serial number and MAC address.
    """)

    with st.form("delete_asset_form"):
        col1, col2 = st.columns(2)

        with col1:
            sn = st.text_input(
                "Serial Number (SN) *",
                help="Device serial number",
                placeholder="e.g., DEVICE-SN-123456"
            )

        with col2:
            mac = st.text_input(
                "MAC Address *",
                help="Device MAC address - accepts colon (:), dash (-), or no separator; uppercase or lowercase",
                placeholder="e.g., AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF"
            )

        deletion_type = st.number_input(
            "Deletion Type",
            min_value=0,
            max_value=10,
            value=0,
            help="Type of deletion operation (optional)"
        )

        submitted = st.form_submit_button("Delete Asset", type="primary")

        if submitted:
            if not sn or not mac:
                st.error("Both Serial Number and MAC Address are required!")
                return

            # Normalize MAC address
            normalized_mac = normalize_mac_address(mac)
            validate_mac_address(normalized_mac, show_warning=True)

            # Show confirmation
            if st.session_state.get('confirm_delete') != f"{sn}_{normalized_mac}":
                st.session_state.confirm_delete = f"{sn}_{normalized_mac}"
                st.warning(f"⚠️ Are you sure you want to delete asset SN: {sn}, MAC: {normalized_mac}?")
                st.info("Click 'Delete Asset' again to confirm.")
                return

            # Call API
            delete_asset(sn=sn, mac=normalized_mac, deletion_type=deletion_type)
            # Clear confirmation
            if 'confirm_delete' in st.session_state:
                del st.session_state.confirm_delete


def delete_asset(sn, mac, deletion_type=None):
    """Execute delete asset API call."""
    try:
        from tauc_openapi.models import DeleteAssetRequest, DeleteAssetResponse
        from tauc_openapi.models.device_asset_management import Asset

        # Show endpoint
        endpoint = "/v1/openapi/device-asset-management/device/delete"
        st.caption(f"📡 Calling: POST {endpoint}")

        # Create request
        request = DeleteAssetRequest(
            asset=Asset(sn=sn, mac=mac),
            deletion_type=deletion_type
        )

        # Execute
        with st.spinner("Deleting asset..."):
            response = st.session_state.client.api_call(
                request,
                DeleteAssetResponse,
                st.session_state.access_token
            )

        if response.is_success():
            if response.result and response.result.failed_assets:
                st.error("Failed to delete asset:")
                for asset in response.result.failed_assets:
                    st.error(f"  - SN: {asset.sn}, MAC: {asset.mac} - Error {asset.error_code}: {asset.message}")
            else:
                st.success("✓ Asset deleted successfully!")

            # Show response
            with st.expander("📄 API Response"):
                st.json({
                    "error_code": response.error_code,
                    "message": response.msg,
                    "failed_assets": len(response.result.failed_assets) if response.result and response.result.failed_assets else 0
                })
        else:
            st.error(f"Failed to delete asset: {response.msg} (Code: {response.error_code})")

    except Exception as e:
        st.error(f"Error deleting asset: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

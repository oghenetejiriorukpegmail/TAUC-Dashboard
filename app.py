"""
TAUC Device Management Dashboard - Beautiful Modern UI
A stunning web-based interface for managing TP-Link network devices via the TAUC OpenAPI.
"""

import streamlit as st
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from theme_css import get_theme_css

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Page configuration
st.set_page_config(
    page_title="TAUC Device Manager",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to get theme-aware colors for inline styles
def get_theme_colors(theme='dark'):
    """Return color values for inline styles based on current theme."""
    if theme == 'dark':
        return {
            'bg_card': '#1f242c',
            'border': '#2f3742',
            'text_primary': '#F5F8FA',
            'text_secondary': 'rgba(245, 248, 250, 0.72)',
            'text_muted': 'rgba(245, 248, 250, 0.55)',
            'accent_primary': '#00BCD4',
            'accent_success': '#10b981',
            'accent_warning': '#f97316',
            'accent_border': 'rgba(0, 188, 212, 0.35)',
        }
    else:
        return {
            'bg_card': '#ffffff',
            'border': '#c5d4e3',
            'text_primary': '#0f172a',
            'text_secondary': 'rgba(15, 23, 42, 0.85)',
            'text_muted': 'rgba(15, 23, 42, 0.68)',
            'accent_primary': '#009fc2',
            'accent_success': '#10b981',
            'accent_warning': '#f97316',
            'accent_border': 'rgba(14, 165, 233, 0.28)',
        }

# Apply theme-specific CSS from imported module
st.markdown(get_theme_css(st.session_state.get('theme', 'dark')), unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'client' not in st.session_state:
    st.session_state.client = None
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'auth_type' not in st.session_state:
    st.session_state.auth_type = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Default to dark mode


def main():
    """Main application entry point with beautiful UI."""

    # Sidebar navigation - Official TAUC Style
    with st.sidebar:
        colors = get_theme_colors(st.session_state.theme)
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem 0 1rem 0;'>
            <h2 style='font-size: 1.5rem; margin: 0; font-weight: 500; color: {colors['text_primary']};'>TP-Link TAUC</h2>
            <p style='color: {colors['text_muted']}; font-size: 0.875rem; margin-top: 0.5rem;'>Device Management</p>
        </div>
        """, unsafe_allow_html=True)

        # Theme toggle
        st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("☀️ Light", use_container_width=True, disabled=(st.session_state.theme == 'light')):
                st.session_state.theme = 'light'
                st.rerun()
        with col2:
            if st.button("🌙 Dark", use_container_width=True, disabled=(st.session_state.theme == 'dark')):
                st.session_state.theme = 'dark'
                st.rerun()
        st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

        if st.session_state.authenticated:
            st.markdown(f"""
            <div class='tauc-status-card' style='margin-bottom: 1.1rem;'>
                <span style='font-weight:600;'>✓ Authenticated</span>
                <span style='font-size:0.8rem; opacity:0.85;'>{st.session_state.auth_type}</span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.client = None
                st.session_state.access_token = None
                st.session_state.auth_type = None
                st.rerun()
        else:
            st.markdown(f"""
            <div class='tauc-status-card warning' style='margin-bottom: 1.1rem;'>
                <span style='font-weight:600;'>⚠ Not Authenticated</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

        # Navigation menu - Clean style
        if st.session_state.authenticated:
            st.markdown(
                f"<p style='font-size: 0.75rem; color: {colors['text_muted']}; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;'>Navigation</p>",
                unsafe_allow_html=True,
            )
            page = st.radio(
                "Select Page",
                ["🏠 Home", "📦 Inventory", "🔧 Network Management", "🔍 Device Lookup",
                 "🌐 Service Activation", "📦 Asset Management"],
                label_visibility="collapsed"
            )
        else:
            page = "🔑 Configuration"

        st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

        # Version footer
        st.markdown("<br>" * 2, unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='text-align: center; color: {colors['text_muted']}; font-size: 0.75rem;'>
                <p style='margin: 0; opacity: 0.75;'>TAUC Dashboard v2.0</p>
                <p style='margin: 0; opacity: 0.6;'>Powered by Streamlit</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Route to appropriate page
    if page == "🔑 Configuration" or not st.session_state.authenticated:
        show_configuration_page()
    elif page == "🏠 Home":
        show_home_page()
    elif page == "📦 Inventory":
        show_inventory_page()
    elif page == "🔧 Network Management":
        show_network_management_page()
    elif page == "🔍 Device Lookup":
        show_device_lookup_page()
    elif page == "🌐 Service Activation":
        show_service_activation_page()
    elif page == "📦 Asset Management":
        show_asset_management_page()


def show_configuration_page():
    """Configuration and authentication page - Official TAUC Style."""

    st.title("🔑 Configuration")
    st.markdown("Configure your TAUC API credentials to get started.")
    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    if st.session_state.authenticated:
        st.success(f"✓ Already authenticated using {st.session_state.auth_type}")
        st.info("Use the sidebar to navigate or logout to reconfigure.")
        return

    # Authentication method selection
    st.markdown("### Authentication Method")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='tauc-card'>
            <h3>OAuth 2.0</h3>
            <p>
                • Recommended for most use cases<br>
                • Secure token-based authentication<br>
                • Automatic token refresh
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='tauc-card'>
            <h3>Access Key / Secret Key</h3>
            <p>
                • For service accounts<br>
                • Direct API access<br>
                • No token management needed
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    auth_method = st.radio(
        "Select Method",
        ["OAuth 2.0", "Access Key/Secret Key"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    # Common settings in beautiful cards
    st.markdown("### ⚙️ Configuration")

    col1, col2 = st.columns(2)

    with col1:
        domain_name = st.text_input(
            "🌐 API Domain",
            value="https://use1-tauc-openapi.tplinkcloud.com",
            help="The TAUC API domain endpoint"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

    # Certificate paths
    default_cert = str(Path(__file__).parent.parent / "certs" / "client.crt")
    default_key = str(Path(__file__).parent.parent / "certs" / "client.key")

    col1, col2 = st.columns(2)

    with col1:
        cert_path = st.text_input(
            "📜 Client Certificate Path",
            value=default_cert,
            help="Absolute path to client.crt file"
        )

    with col2:
        key_path = st.text_input(
            "🔑 Client Key Path",
            value=default_key,
            help="Absolute path to client.key file"
        )

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    # Authentication-specific fields
    if auth_method == "OAuth 2.0":
        st.markdown("### OAuth 2.0 Credentials")

        # Load from .env if available
        env_client_id = os.getenv("TAUC_CLIENT_ID", "")
        env_client_secret = os.getenv("TAUC_CLIENT_SECRET", "")

        if env_client_id:
            st.success("✓ Credentials loaded from .env file")

        col1, col2 = st.columns(2)
        with col1:
            client_id = st.text_input("Client ID", value=env_client_id, type="password")
        with col2:
            client_secret = st.text_input("Client Secret", value=env_client_secret, type="password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Authenticate with OAuth 2.0", type="primary", use_container_width=False):
            if not all([client_id, client_secret, domain_name, cert_path, key_path]):
                st.error("All fields are required!")
            else:
                authenticate_oauth(client_id, client_secret, domain_name, cert_path, key_path)

    else:  # AK/SK
        st.markdown("### Access Key / Secret Key Credentials")

        # Load from .env if available
        env_access_key = os.getenv("TAUC_ACCESS_KEY", "")
        env_secret_key = os.getenv("TAUC_SECRET_KEY", "")

        if env_access_key:
            st.success("✓ Credentials loaded from .env file")

        col1, col2 = st.columns(2)
        with col1:
            access_key = st.text_input("Access Key", value=env_access_key, type="password")
        with col2:
            secret_key = st.text_input("Secret Key", value=env_secret_key, type="password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Authenticate with AK/SK", type="primary", use_container_width=False):
            if not all([access_key, secret_key, domain_name, cert_path, key_path]):
                st.error("All fields are required!")
            else:
                authenticate_aksk(access_key, secret_key, domain_name, cert_path, key_path)


def authenticate_oauth(client_id, client_secret, domain_name, cert_path, key_path):
    """Authenticate using OAuth 2.0."""
    try:
        from tauc_openapi import ApiClient
        from tauc_openapi.models import GetAccessTokenRequest, GetAccessTokenResponse

        with st.spinner("🔄 Authenticating..."):
            # Build client
            client = ApiClient.build_oauth_client(
                client_id=client_id,
                client_secret=client_secret,
                domain_name=domain_name,
                client_cert_path=cert_path,
                client_key_path=key_path
            )

            # Get access token
            token_request = GetAccessTokenRequest()
            token_response = client.access_token_call(token_request, GetAccessTokenResponse)

            if not token_response.is_success():
                st.error(f"❌ Authentication failed: {token_response.msg} (Code: {token_response.error_code})")
                return

            # Validate access token was returned
            if not token_response.result or not token_response.result.access_token:
                st.error("❌ Authentication succeeded but no access token was returned.")
                return

            # Store in session
            st.session_state.client = client
            st.session_state.access_token = token_response.result.access_token
            st.session_state.authenticated = True
            st.session_state.auth_type = "OAuth 2.0"

            st.success("✅ Authentication successful!")
            st.balloons()
            st.rerun()

    except Exception as e:
        st.error(f"❌ Authentication error: {str(e)}")


def authenticate_aksk(access_key, secret_key, domain_name, cert_path, key_path):
    """Authenticate using Access Key/Secret Key."""
    try:
        from tauc_openapi import ApiClient

        with st.spinner("🔄 Initializing client..."):
            # Build client
            client = ApiClient.build_aksk_client(
                access_key=access_key,
                secret_key=secret_key,
                domain_name=domain_name,
                client_cert_path=cert_path,
                client_key_path=key_path
            )

            # Store in session
            st.session_state.client = client
            st.session_state.access_token = None
            st.session_state.authenticated = True
            st.session_state.auth_type = "AK/SK"

            st.success("✅ Client initialized successfully!")
            st.balloons()
            st.rerun()

    except Exception as e:
        st.error(f"❌ Initialization error: {str(e)}")


def show_home_page():
    """Home page - Official TAUC Style."""

    operator_name = (
        st.session_state.get('operator_name')
        or os.getenv('TAUC_OPERATOR_NAME')
        or os.getenv('TAUC_ACCOUNT_EMAIL')
        or "Operator"
    )

    hour = datetime.now().hour
    if hour < 12:
        salutation = "Good morning"
    elif hour < 18:
        salutation = "Good afternoon"
    else:
        salutation = "Good evening"

    st.markdown(
        f"""
        <div class='tauc-hero'>
            <h1>{salutation}, {operator_name}</h1>
            <p>Monitor network health, deployment status, and authentication at a glance.</p>
            <div style='display:flex;flex-wrap:wrap;gap:0.6rem;margin-top:1.1rem;'>
                <span class='tauc-chip success'>✓ Authenticated &nbsp;•&nbsp; {st.session_state.auth_type}</span>
                <span class='tauc-chip'>Session Active</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nat_locked_total = None
    try:
        from tauc_openapi.models import GetNATLockedInventoryRequest, GetNATLockedInventoryResponse

        request = GetNATLockedInventoryRequest(page="0", pageSize="1")
        response = st.session_state.client.api_call(
            request,
            GetNATLockedInventoryResponse,
            st.session_state.access_token
        )

        if response.is_success():
            nat_locked_total = response.result.total or 0
    except Exception:
        nat_locked_total = None

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_value = "—" if nat_locked_total is None else nat_locked_total
        st.markdown(
            f"""
            <div class='metric-card'>
                <p>NAT-Locked Devices</p>
                <h3>{metric_value}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class='metric-card'>
                <p>Authentication</p>
                <h3 style='font-size:1.45rem;'>{st.session_state.auth_type}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class='metric-card'>
                <p>Status</p>
                <h3 class='status-online'>Connected</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class='metric-card'>
                <p>Environment</p>
                <h3 style='font-size:1.45rem;'>{os.getenv('TAUC_ENV', 'Production')}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='tauc-divider'></div>", unsafe_allow_html=True)

    st.markdown("### Available Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class='tauc-card'>
                <h3>📦 Inventory</h3>
                <p>
                    • Browse network inventory with status filters<br>
                    • Export network and device data<br>
                    • Surface NAT-locked networks instantly
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='tauc-card' style='margin-top: 1rem;'>
                <h3>🔧 Network Management</h3>
                <p>
                    • Lock or unlock NAT in real time<br>
                    • Inspect network status & metadata<br>
                    • Trigger targeted actions safely
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class='tauc-card'>
                <h3>🔍 Device Lookup</h3>
                <p>
                    • Search by MAC or serial number<br>
                    • Retrieve device fingerprints<br>
                    • Copy identifiers for support flows
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='tauc-card' style='margin-top: 1rem;'>
                <h3>🌐 Service Activation</h3>
                <p>
                    • Onboard single or batch networks<br>
                    • Configure wireless defaults<br>
                    • Track provisioning progress
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class='tauc-card'>
                <h3>📦 Asset Management</h3>
                <p>
                    • Register and update device assets<br>
                    • Process batch import tasks<br>
                    • Track failures for follow-up
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='tauc-card' style='margin-top: 1rem;'>
                <h3>📊 Data Export</h3>
                <p>
                    • Download CSV summaries<br>
                    • Share JSON payloads for support<br>
                    • Keep audits structured and fast
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_inventory_page():
    """Inventory management page."""
    from pages import inventory
    inventory.show()


def show_network_management_page():
    """Network management page."""
    from pages import network_management
    network_management.show()


def show_device_lookup_page():
    """Device lookup page."""
    from pages import device_lookup
    device_lookup.show()


def show_service_activation_page():
    """Service activation page."""
    from pages import service_activation
    service_activation.show()


def show_asset_management_page():
    """Asset management page."""
    from pages import asset_management
    asset_management.show()


if __name__ == "__main__":
    main()

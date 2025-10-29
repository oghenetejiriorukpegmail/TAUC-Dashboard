"""Theme CSS generator for TAUC Dashboard."""


def get_theme_css(theme: str = 'dark') -> str:
    """Generate CSS matching the TP-Link TAUC aesthetic."""

    if theme == 'dark':
        colors = {
            'bg_main': '#182130',
            'bg_sidebar': '#1d2735',
            'bg_card': '#212d3f',
            'bg_hover': '#27364a',
            'border': '#2e3b4f',
            'border_soft': 'rgba(255, 255, 255, 0.1)',
            'text_primary': '#f7fbff',
            'text_secondary': 'rgba(227, 240, 255, 0.78)',
            'text_muted': 'rgba(201, 214, 232, 0.6)',
            'primary': '#38bdf8',
            'primary_hover': '#0ea5e9',
            'primary_soft': 'rgba(56, 189, 248, 0.22)',
            'accent': '#7dd3fc',
            'chart_from': 'rgba(56, 189, 248, 0.2)',
            'chart_to': 'rgba(56, 189, 248, 0.05)',
            'scrollbar_track': '#101522',
            'table_header': 'rgba(38, 51, 69, 0.92)',
            'table_text': 'rgba(232, 242, 255, 0.94)',
            'table_muted': 'rgba(209, 225, 245, 0.7)',
            'table_row_hover': 'rgba(56, 189, 248, 0.18)',
            'table_row_bg': 'rgba(30, 41, 55, 0.9)',
            'table_row_even': 'rgba(24, 33, 46, 0.92)',
            'input_text': '#f7fbff',
            'tab_text': 'rgba(227, 240, 255, 0.78)',
            'metric_label': 'rgba(209, 225, 245, 0.78)',
            'card_metric_label': 'rgba(209, 225, 245, 0.72)',
            'chip_success': 'rgba(16, 185, 129, 0.14)',
            'chip_error': 'rgba(248, 113, 113, 0.14)',
            'chip_border': 'rgba(255, 255, 255, 0.08)',
            'shadow': '0 24px 55px -32px rgba(6, 11, 24, 0.82)',
            'shadow_soft': '0 20px 42px -30px rgba(6, 11, 24, 0.6)',
            'hero_start': 'rgba(56, 189, 248, 0.24)',
            'hero_mid': 'rgba(125, 211, 252, 0.18)',
            'hero_end': 'rgba(186, 230, 253, 0.22)',
            'card_start': 'rgba(33, 45, 63, 0.94)',
            'card_end': 'rgba(28, 38, 55, 0.96)',
            'metric_start': 'rgba(56, 189, 248, 0.22)',
            'metric_mid': 'rgba(125, 211, 252, 0.18)',
            'metric_end': 'rgba(186, 230, 253, 0.16)',
            'notification_start': 'rgba(35, 48, 66, 0.94)',
            'notification_end': 'rgba(24, 34, 49, 0.95)',
            'status_primary_start': 'rgba(56, 189, 248, 0.26)',
            'status_primary_end': 'rgba(125, 211, 252, 0.22)',
            'status_warning_start': 'rgba(245, 158, 11, 0.28)',
            'status_warning_end': 'rgba(251, 191, 36, 0.22)',
            'status_primary_border': 'rgba(56, 189, 248, 0.38)',
            'status_warning_border': 'rgba(251, 191, 36, 0.4)',
            'download_bg': 'rgba(56, 189, 248, 0.22)',
            'download_hover': 'rgba(56, 189, 248, 0.32)',
            'code_bg': '#0c121c',
            'code_border': 'rgba(148, 163, 184, 0.18)',
            'code_text': '#e2e8f0',
            'input_bg': '#212d3f',
            'input_border': '#2e3b4f',
            'input_placeholder': 'rgba(201, 214, 232, 0.6)',
            'input_caret': '#f7fbff',
            'button_text': '#0f172a'
        }
    else:
        colors = {
            'bg_main': '#f6f9fd',
            'bg_sidebar': '#ffffff',
            'bg_card': '#ffffff',
            'bg_hover': '#eef3f9',
            'border': '#c5d4e3',
            'border_soft': 'rgba(15, 23, 42, 0.12)',
            'text_primary': '#0f172a',
            'text_secondary': 'rgba(15, 23, 42, 0.90)',
            'text_muted': 'rgba(15, 23, 42, 0.68)',
            'primary': '#38bdf8',
            'primary_hover': '#0ea5e9',
            'primary_soft': 'rgba(56, 189, 248, 0.18)',
            'accent': '#7dd3fc',
            'chart_from': 'rgba(56, 189, 248, 0.18)',
            'chart_to': 'rgba(56, 189, 248, 0.04)',
            'scrollbar_track': '#d3deea',
            'table_header': '#e3ecf5',
            'table_text': 'rgba(15, 23, 42, 0.9)',
            'table_muted': 'rgba(15, 23, 42, 0.7)',
            'table_row_hover': 'rgba(56, 189, 248, 0.08)',
            'table_row_bg': '#ffffff',
            'table_row_even': '#f8fafb',
            'input_text': '#0f172a',
            'tab_text': 'rgba(15, 23, 42, 0.88)',
            'metric_label': 'rgba(15, 23, 42, 0.75)',
            'card_metric_label': 'rgba(15, 23, 42, 0.75)',
            'chip_success': 'rgba(16, 185, 129, 0.20)',
            'chip_error': 'rgba(248, 113, 113, 0.20)',
            'chip_border': 'rgba(15, 23, 42, 0.22)',
            'shadow': '0 16px 32px -26px rgba(15, 23, 42, 0.28)',
            'shadow_soft': '0 12px 26px -24px rgba(15, 23, 42, 0.2)',
            'hero_start': '#ecf7ff',
            'hero_mid': '#f5fbff',
            'hero_end': '#f0fdfa',
            'card_start': '#ffffff',
            'card_end': '#f8fbff',
            'metric_start': '#ecf7ff',
            'metric_mid': '#f5fbff',
            'metric_end': '#f0fdfa',
            'notification_start': '#ffffff',
            'notification_end': '#f3f8ff',
            'status_primary_start': '#e4f6ff',
            'status_primary_end': '#f0fdfa',
            'status_warning_start': '#fff7e6',
            'status_warning_end': '#fff1d6',
            'status_primary_border': 'rgba(56, 189, 248, 0.35)',
            'status_warning_border': 'rgba(251, 191, 36, 0.40)',
            'download_bg': 'rgba(56, 189, 248, 0.28)',
            'download_hover': 'rgba(56, 189, 248, 0.38)',
            'code_bg': '#eef3fa',
            'code_border': 'rgba(15, 23, 42, 0.15)',
            'code_text': '#10213a',
            'metric_text': '#0f172a',
            'metric_accent': '#0ea5e9',
            'input_bg': '#ffffff',
            'input_border': 'rgba(15, 23, 42, 0.35)',
            'input_placeholder': 'rgba(15, 23, 42, 0.58)',
            'input_caret': '#0f172a',
            'button_text': '#475569'
        }

    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0&display=swap');

    body, div, span, input, textarea, button {{
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    input, textarea, select {{
        caret-color: var(--tauc-input-caret);
        color: var(--tauc-text-secondary);
    }}

    body, .stMarkdown, .stMarkdown p, .stMarkdown li, label, .st-ck, .stText, .stCaption, .streamlit-expanderContent, .stSelectbox div, .stNumberInput label {{
        color: var(--tauc-text-secondary);
    }}

    strong, b {{
        color: var(--tauc-text-primary) !important;
    }}

    body {{
        background: var(--tauc-bg-main);
        color: var(--tauc-text-primary);
    }}

    .stApp {{
        background: var(--tauc-bg-main);
    }}

    .material-icons,
    .material-icons-round,
    .material-icons-outlined,
    .material-symbols-outlined,
    .material-symbols-rounded {{
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons Round', 'Material Icons' !important;
        font-weight: normal;
        font-style: normal;
        font-size: inherit;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        font-feature-settings: 'liga';
    }}

    .material-symbols-outlined {{
        font-family: 'Material Symbols Outlined' !important;
    }}

    .material-symbols-rounded {{
        font-family: 'Material Symbols Rounded' !important;
    }}

    .material-icons {{
        font-family: 'Material Icons' !important;
    }}

    .material-icons-round {{
        font-family: 'Material Icons Round' !important;
    }}

    .material-icons-outlined {{
        font-family: 'Material Icons Outlined' !important;
    }}

    :root {{
        --tauc-bg-main: {colors['bg_main']};
        --tauc-bg-sidebar: {colors['bg_sidebar']};
        --tauc-bg-card: {colors['bg_card']};
        --tauc-bg-hover: {colors['bg_hover']};
        --tauc-border: {colors['border']};
        --tauc-border-soft: {colors['border_soft']};
        --tauc-text-primary: {colors['text_primary']};
        --tauc-text-secondary: {colors['text_secondary']};
        --tauc-text-muted: {colors['text_muted']};
        --tauc-primary: {colors['primary']};
        --tauc-primary-hover: {colors['primary_hover']};
        --tauc-primary-soft: {colors['primary_soft']};
        --tauc-accent: {colors['accent']};
        --tauc-chart-from: {colors['chart_from']};
        --tauc-chart-to: {colors['chart_to']};
        --tauc-table-header: {colors['table_header']};
        --tauc-table-text: {colors['table_text']};
        --tauc-table-muted: {colors['table_muted']};
        --tauc-table-hover: {colors['table_row_hover']};
        --tauc-table-row-bg: {colors.get('table_row_bg', colors['bg_card'])};
        --tauc-table-row-even: {colors.get('table_row_even', colors.get('table_row_bg', colors['bg_card']))};
        --tauc-chip-success: {colors['chip_success']};
        --tauc-chip-error: {colors['chip_error']};
        --tauc-chip-border: {colors['chip_border']};
        --tauc-shadow: {colors['shadow']};
        --tauc-shadow-soft: {colors['shadow_soft']};
        --tauc-hero-start: {colors['hero_start']};
        --tauc-hero-mid: {colors['hero_mid']};
        --tauc-hero-end: {colors['hero_end']};
        --tauc-card-start: {colors['card_start']};
        --tauc-card-end: {colors['card_end']};
        --tauc-metric-start: {colors['metric_start']};
        --tauc-metric-mid: {colors['metric_mid']};
        --tauc-metric-end: {colors['metric_end']};
        --tauc-notification-start: {colors['notification_start']};
        --tauc-notification-end: {colors['notification_end']};
        --tauc-status-primary-start: {colors['status_primary_start']};
        --tauc-status-primary-end: {colors['status_primary_end']};
        --tauc-status-warning-start: {colors['status_warning_start']};
        --tauc-status-warning-end: {colors['status_warning_end']};
        --tauc-status-border: {colors['status_primary_border']};
        --tauc-status-warning-border: {colors['status_warning_border']};
        --tauc-download-bg: {colors['download_bg']};
        --tauc-download-hover: {colors['download_hover']};
        --tauc-code-bg: {colors['code_bg']};
        --tauc-code-border: {colors['code_border']};
        --tauc-code-text: {colors['code_text']};
        --tauc-metric-text: {colors.get('metric_text', colors['text_primary'])};
        --tauc-metric-accent: {colors.get('metric_accent', colors['primary'])};
        --tauc-input-bg: {colors['input_bg']};
        --tauc-input-border: {colors['input_border']};
        --tauc-input-placeholder: {colors['input_placeholder']};
        --tauc-input-caret: {colors['input_caret']};
        --tauc-button-text: {colors['button_text']};
    }}

    .main {{
        background: linear-gradient(180deg, rgba(7, 89, 133, 0.03) 0%, rgba(7, 89, 133, 0) 85%), var(--tauc-bg-main);
        padding: 0;
    }}

    .main .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }}

    [data-testid="stSidebar"] {{
        background: var(--tauc-bg-sidebar) !important;
        border-right: 1px solid var(--tauc-border) !important;
        min-width: 21rem !important;
        display: block !important;
        visibility: visible !important;
    }}

    [data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] {{
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }}

    /* Sidebar Navigation Links - ULTRA ENHANCED Contrast */
    [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] nav,
    [data-testid="stSidebar"] nav {{
        padding-top: 1rem;
    }}

    /* All navigation links and buttons */
    [data-testid="stSidebarNav"] a,
    [data-testid="stSidebarNav"] [role="button"],
    [data-testid="stSidebar"] nav a,
    [data-testid="stSidebar"] nav button,
    [data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] button {{
        color: var(--tauc-text-primary) !important;
        text-decoration: none !important;
        font-weight: 500 !important;
        opacity: 1 !important;
    }}

    /* Hover states */
    [data-testid="stSidebarNav"] a:hover,
    [data-testid="stSidebarNav"] [role="button"]:hover,
    [data-testid="stSidebar"] nav a:hover {{
        background-color: var(--tauc-bg-hover) !important;
        color: var(--tauc-primary) !important;
    }}

    /* All SVG icons and spans - MAXIMUM CONTRAST */
    [data-testid="stSidebarNav"] svg,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebar"] nav svg,
    [data-testid="stSidebar"] nav span,
    section[data-testid="stSidebar"] svg,
    section[data-testid="stSidebar"] nav svg,
    [data-testid="stSidebar"] ul svg,
    [data-testid="stSidebar"] li svg {{
        color: var(--tauc-text-primary) !important;
        fill: var(--tauc-text-primary) !important;
        stroke: var(--tauc-text-primary) !important;
        opacity: 1 !important;
    }}

    /* Navigation item text - all possible selectors */
    [data-testid="stSidebarNav"] ul li a span,
    [data-testid="stSidebarNav"] ul li div span,
    [data-testid="stSidebar"] nav ul li span,
    [data-testid="stSidebar"] li span,
    section[data-testid="stSidebar"] span {{
        color: var(--tauc-text-primary) !important;
        font-weight: 500 !important;
        opacity: 1 !important;
    }}

    /* Direct SVG path elements */
    [data-testid="stSidebarNav"] svg path,
    [data-testid="stSidebar"] svg path,
    section[data-testid="stSidebar"] svg path {{
        fill: var(--tauc-text-primary) !important;
        stroke: var(--tauc-text-primary) !important;
        opacity: 1 !important;
    }}

    /* List items in sidebar */
    [data-testid="stSidebar"] ul li,
    [data-testid="stSidebarNav"] ul li {{
        color: var(--tauc-text-primary) !important;
    }}

    /* Streamlit page link specific */
    [data-testid="stPageLink"],
    [data-testid="stPageLink"] span,
    [data-testid="stPageLink"] svg,
    [data-testid="stPageLink"] svg path {{
        color: var(--tauc-text-primary) !important;
        fill: var(--tauc-text-primary) !important;
        stroke: var(--tauc-text-primary) !important;
        opacity: 1 !important;
    }}

    h1, h2, h3, h4 {{
        color: var(--tauc-text-primary) !important;
        font-weight: 500 !important;
    }}

    h1 {{ font-size: 1.9rem !important; }}
    h2 {{ font-size: 1.45rem !important; }}
    h3 {{ font-size: 1.2rem !important; }}

    .stAlert {{
        border-radius: 14px;
        border-left: 4px solid var(--tauc-primary);
        background: var(--tauc-bg-card) !important;
        box-shadow: var(--tauc-shadow);
        color: var(--tauc-text-primary);
    }}

    .stSuccess {{
        background: linear-gradient(135deg, var(--tauc-status-primary-start) 0%, var(--tauc-status-primary-end) 100%) !important;
        border-left: 4px solid var(--tauc-status-border) !important;
        color: var(--tauc-text-primary) !important;
    }}

    .stError {{
        background: linear-gradient(135deg, rgba(244, 63, 94, 0.2) 0%, rgba(239, 68, 68, 0.24) 100%) !important;
        border-left: 4px solid rgba(239, 68, 68, 0.58) !important;
        color: var(--tauc-text-primary) !important;
    }}

    .stInfo {{
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.18) 0%, rgba(37, 99, 235, 0.2) 100%) !important;
        border-left: 4px solid rgba(59, 130, 246, 0.55) !important;
        color: var(--tauc-text-primary) !important;
    }}

    .stWarning {{
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(245, 158, 11, 0.22) 100%) !important;
        border-left: 4px solid #fbbf24 !important;
        color: var(--tauc-text-primary) !important;
    }}

    /* ULTRA-NUCLEAR BUTTON STYLING - Overrides EVERYTHING */
    /* Use multiple selector chains to maximize specificity */
    button:not([aria-hidden="true"]):not([tabindex="-1"]),
    button[type]:not([aria-hidden="true"]),
    button:not([type]):not([aria-hidden="true"]),
    div button:not([aria-hidden="true"]),
    section button:not([aria-hidden="true"]),
    .stButton button,
    .stButton > button,
    .stButton button[type],
    .stForm button,
    .stForm > * button,
    button[kind="primary"],
    button[kind="secondary"],
    button[kind="tertiary"],
    button[data-testid*="baseButton"],
    button[data-testid*="FormSubmit"],
    button[data-testid*="Button"],
    button[class*="Button"],
    button[class*="button"],
    div[class*="stButton"] button,
    div[class*="stButton"] > button,
    div[data-testid*="stButton"] button,
    [role="button"]:not(a):not(div):not(span) {{
        border-radius: 14px !important;
        border: 1px solid transparent !important;
        background: linear-gradient(90deg, var(--tauc-primary) 0%, var(--tauc-accent) 100%) !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.6rem !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--tauc-shadow-soft) !important;
        text-decoration: none !important;
    }}

    /* Force ALL button text content to use button text color */
    button:not([aria-hidden="true"]) *,
    button:not([tabindex="-1"]) *,
    .stButton button span,
    .stButton button div,
    .stButton button p,
    .stButton > button span,
    .stButton > button div,
    .stButton > button p,
    button[data-testid*="Button"] span,
    button[data-testid*="Button"] div,
    button[data-testid*="Button"] p,
    button[data-testid*="Button"] *,
    .stForm button span,
    .stForm button div,
    .stForm button p,
    .stForm button *,
    [role="button"]:not([aria-hidden="true"]) span,
    [role="button"]:not([aria-hidden="true"]) div,
    [role="button"]:not([aria-hidden="true"]) p,
    [role="button"]:not([aria-hidden="true"]) * {{
        color: inherit !important;
    }}

    .stButton button svg,
    .stButton > button svg,
    button[data-testid*="Button"] svg {{
        fill: inherit !important;
        color: inherit !important;
    }}

    /* HOVER states - ALL buttons - ULTRA-SPECIFIC */
    button:hover:not(:disabled):not([aria-hidden="true"]),
    button[type]:hover:not(:disabled):not([aria-hidden="true"]),
    button:not([type]):hover:not(:disabled):not([aria-hidden="true"]),
    div button:hover:not(:disabled):not([aria-hidden="true"]),
    section button:hover:not(:disabled):not([aria-hidden="true"]),
    .stButton button:hover:not(:disabled),
    .stButton > button:hover:not(:disabled),
    .stForm button:hover:not(:disabled),
    .stForm > * button:hover:not(:disabled),
    button[kind="primary"]:hover:not(:disabled),
    button[kind="secondary"]:hover:not(:disabled),
    button[kind="tertiary"]:hover:not(:disabled),
    button[data-testid*="baseButton"]:hover:not(:disabled),
    button[data-testid*="FormSubmit"]:hover:not(:disabled),
    button[data-testid*="Button"]:hover:not(:disabled),
    button[class*="Button"]:hover:not(:disabled),
    button[class*="button"]:hover:not(:disabled),
    div[class*="stButton"] button:hover:not(:disabled),
    div[data-testid*="stButton"] button:hover:not(:disabled),
    [role="button"]:hover:not(a):not(div):not(span):not(:disabled) {{
        background: linear-gradient(90deg, var(--tauc-primary-hover) 0%, var(--tauc-accent) 100%) !important;
        box-shadow: 0 6px 16px -6px var(--tauc-primary) !important;
        transform: translateY(-1px) !important;
        border-color: var(--tauc-primary) !important;
        color: #0f172a !important;
    }}

    /* Force ALL button text content to inherit color on HOVER too */
    button:hover:not(:disabled) *,
    .stButton button:hover:not(:disabled) span,
    .stButton button:hover:not(:disabled) div,
    .stButton button:hover:not(:disabled) p,
    .stButton button:hover:not(:disabled) *,
    button[data-testid*="Button"]:hover:not(:disabled) *,
    .stForm button:hover:not(:disabled) * {{
        color: inherit !important;
    }}

    /* DISABLED states - ALL buttons - ULTRA-SPECIFIC */
    button:disabled:not([aria-hidden="true"]),
    button[type]:disabled:not([aria-hidden="true"]),
    button:not([type]):disabled:not([aria-hidden="true"]),
    div button:disabled:not([aria-hidden="true"]),
    section button:disabled:not([aria-hidden="true"]),
    .stButton button:disabled,
    .stButton > button:disabled,
    .stForm button:disabled,
    .stForm > * button:disabled,
    button[kind="primary"]:disabled,
    button[kind="secondary"]:disabled,
    button[kind="tertiary"]:disabled,
    button[data-testid*="baseButton"]:disabled,
    button[data-testid*="FormSubmit"]:disabled,
    button[data-testid*="Button"]:disabled,
    button[class*="Button"]:disabled,
    button[class*="button"]:disabled,
    div[class*="stButton"] button:disabled,
    div[data-testid*="stButton"] button:disabled,
    button[disabled]:not([aria-hidden="true"]),
    button[aria-disabled="true"]:not([aria-hidden="true"]) {{
        background: var(--tauc-bg-hover) !important;
        color: var(--tauc-text-muted) !important;
        border: 1px solid var(--tauc-border) !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
        transform: none !important;
    }}

    /* FINAL NUCLEAR CATCH-ALL - Maximum specificity */
    :is(button, [role="button"]):is(:not([aria-hidden="true"])):is(:not([tabindex="-1"])) {{
        background: linear-gradient(90deg, var(--tauc-primary) 0%, var(--tauc-accent) 100%) !important;
        color: #0f172a !important;
        border-radius: 14px !important;
        border: 1px solid transparent !important;
        font-weight: 500 !important;
        padding: 0.55rem 1.6rem !important;
    }}

    :is(button, [role="button"]):is(:disabled) {{
        background: var(--tauc-bg-hover) !important;
        color: var(--tauc-text-muted) !important;
        opacity: 0.6 !important;
    }}

    /* ABSOLUTE FINAL CATCH-ALL - Force ALL button children to inherit button color */
    :is(button, [role="button"]):is(:not([aria-hidden="true"])):is(:not([tabindex="-1"])) * {{
        color: inherit !important;
    }}

    :is(button, [role="button"]):is(:not([aria-hidden="true"])):is(:not([tabindex="-1"])):hover:not(:disabled) * {{
        color: inherit !important;
    }}

    /* ULTRA-NUCLEAR STREAMLIT-SPECIFIC BUTTON TEXT */
    div[class*="stButton"] button > div[data-testid="stMarkdownContainer"],
    div[class*="stButton"] button > div[data-testid="stMarkdownContainer"] *,
    button[data-testid*="baseButton"] > div,
    button[data-testid*="baseButton"] > div *,
    button[data-testid*="FormSubmit"] > div,
    button[data-testid*="FormSubmit"] > div *,
    button[kind] > div,
    button[kind] > div * {{
        color: inherit !important;
        fill: inherit !important;
    }}

    div[data-testid="stDownloadButton"] > button {{
        border-radius: 12px;
        border: 1px solid transparent;
        padding: 0.55rem 1.4rem;
        font-weight: 500;
        background: var(--tauc-download-bg);
        color: var(--tauc-text-primary);
        box-shadow: var(--tauc-shadow-soft);
    }}

    div[data-testid="stDownloadButton"] > button:hover {{
        background: var(--tauc-download-hover);
        border-color: var(--tauc-primary);
    }}

    /* TOOLTIP STYLING - Ensure tooltips are readable */
    /* Streamlit tooltip components */
    .stTooltipContent,
    [role="tooltip"],
    [data-testid="stTooltipContent"],
    div[class*="tooltip" i],
    div[class*="Tooltip" i] {{
        background: rgba(15, 23, 42, 0.95) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}

    /* Tooltip text elements */
    .stTooltipContent *,
    [role="tooltip"] *,
    [data-testid="stTooltipContent"] * {{
        color: #ffffff !important;
    }}

    /* Button title attributes (native browser tooltips) */
    button[title],
    button[data-title],
    [role="button"][title] {{
        position: relative;
    }}

    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {{
        border-radius: 12px;
        border: 1px solid var(--tauc-input-border);
        background: var(--tauc-input-bg);
        color: var(--tauc-text-primary);
        padding: 0.65rem 0.9rem;
    }}

    [data-baseweb="select"] > div:first-child {{
        border-radius: 12px;
        border: 1px solid var(--tauc-input-border);
        background: var(--tauc-input-bg);
        color: var(--tauc-text-primary);
        box-shadow: none;
    }}

    [data-baseweb="select"] > div:first-child > div {{
        color: var(--tauc-text-primary);
    }}

    [data-baseweb="select"] svg {{
        fill: var(--tauc-text-primary);
    }}

    .stTextInput input::placeholder,
    .stSelectbox select option,
    textarea::placeholder {{
        color: var(--tauc-input-placeholder);
    }}

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--tauc-primary);
        box-shadow: 0 0 0 1px var(--tauc-primary);
        caret-color: var(--tauc-input-caret);
    }}

    [data-baseweb="select"]:focus-within > div:first-child {{
        border-color: var(--tauc-primary);
        box-shadow: 0 0 0 1px var(--tauc-primary);
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.9rem !important;
        font-weight: 600 !important;
        color: var(--tauc-metric-accent) !important;
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 0.85rem !important;
        color: var(--tauc-metric-text) !important;
        text-transform: uppercase;
        letter-spacing: 0.45px;
    }}

    .tauc-card {{
        background: linear-gradient(160deg, var(--tauc-card-start) 0%, var(--tauc-card-end) 100%);
        border: 1px solid var(--tauc-border-soft);
        border-radius: 18px;
        padding: 1.4rem 1.6rem;
        box-shadow: var(--tauc-shadow);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: var(--tauc-text-secondary);
    }}

    .tauc-card h3 {{
        color: var(--tauc-text-primary) !important;
        font-weight: 600 !important;
        margin-bottom: 0.55rem !important;
    }}

    .tauc-card p {{
        color: var(--tauc-text-secondary);
    }}

    .tauc-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 28px 48px -32px rgba(15, 23, 42, 0.6);
        border-color: var(--tauc-status-border);
    }}

    .tauc-status-card {{
        background: linear-gradient(135deg, var(--tauc-status-primary-start) 0%, var(--tauc-status-primary-end) 100%);
        border-radius: 16px;
        padding: 0.9rem 1.1rem;
        border: 1px solid var(--tauc-status-border);
        box-shadow: var(--tauc-shadow-soft);
        text-align: center;
    }}

    .tauc-status-card.warning {{
        background: linear-gradient(135deg, var(--tauc-status-warning-start) 0%, var(--tauc-status-warning-end) 100%);
        border-color: var(--tauc-status-warning-border);
    }}

    .tauc-status-card span {{
        display: block;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
        color: var(--tauc-text-primary);
    }}

    /* Sidebar navigation styling */
    [data-testid="stSidebar"] .stRadio > div {{
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }}

    [data-testid="stSidebar"] .stRadio > div > label {{
        border: 1px solid var(--tauc-border);
        background: var(--tauc-bg-card);
        border-radius: 12px;
        padding: 0.55rem 0.95rem;
        color: var(--tauc-text-secondary);
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: none;
    }}

    [data-testid="stSidebar"] .stRadio > div > label:hover {{
        border-color: var(--tauc-primary);
        background: var(--tauc-bg-hover);
        color: var(--tauc-text-primary);
        box-shadow: var(--tauc-shadow-soft);
    }}

    [data-testid="stSidebar"] .stRadio > div > label:has(> input:checked) {{
        border-color: var(--tauc-primary);
        background: linear-gradient(135deg, var(--tauc-status-primary-start) 0%, var(--tauc-status-primary-end) 100%);
        color: var(--tauc-text-primary);
        box-shadow: var(--tauc-shadow);
    }}

    [data-testid="stSidebar"] .stRadio > div > label > input {{
        display: none;
    }}

    [data-testid="stSidebar"] .stRadio > div > label span {{
        font-size: 0.95rem !important;
        color: inherit !important;
    }}

    [data-testid="stSidebar"] .stRadio > div > label div {{
        color: inherit !important;
    }}

    .metric-card {{
        background: linear-gradient(150deg, var(--tauc-metric-start) 0%, var(--tauc-metric-mid) 45%, var(--tauc-metric-end) 100%);
        border-radius: 18px;
        padding: 1.55rem;
        border: 1px solid var(--tauc-border-soft);
        box-shadow: var(--tauc-shadow-soft);
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }}

    .metric-card p {{
        font-size: 0.8rem;
        letter-spacing: 0.3px;
        color: var(--tauc-metric-text);
        margin: 0;
        text-transform: uppercase;
    }}

    .metric-card h3 {{
        font-size: 2.05rem;
        margin: 0;
        color: var(--tauc-metric-accent);
        font-weight: 600;
    }}

    .tauc-hero {{
        background: linear-gradient(115deg, var(--tauc-hero-start) 0%, var(--tauc-hero-mid) 45%, var(--tauc-hero-end) 100%);
        border: 1px solid var(--tauc-border-soft);
        border-radius: 24px;
        padding: 1.9rem 2.2rem;
        margin-bottom: 1.6rem;
        box-shadow: var(--tauc-shadow);
    }}

    .tauc-hero h1 {{
        margin-bottom: 0.35rem;
        font-size: 1.95rem !important;
    }}

    .tauc-hero p {{
        margin: 0;
        color: var(--tauc-text-secondary);
        font-size: 0.98rem;
    }}

    .stTabs [role="tablist"] {{
        gap: 0.4rem;
        border-bottom: none;
        margin-bottom: 1rem;
    }}

    .stTabs [role="tab"] {{
        background: var(--tauc-bg-card);
        border-radius: 14px;
        border: 1px solid transparent;
        padding: 0.55rem 1.35rem;
        font-weight: 500;
        color: var(--tauc-text-secondary) !important;
        transition: all 0.2s ease;
    }}

    .stTabs [role="tab"][aria-selected="true"] {{
        border-color: var(--tauc-primary);
        box-shadow: 0 18px 32px -24px rgba(0, 188, 212, 0.8);
        color: var(--tauc-primary) !important;
    }}

    .tauc-chip {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        border-radius: 999px;
        padding: 0.25rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 500;
        border: 1px solid var(--tauc-chip-border);
        color: var(--tauc-text-secondary);
    }}

    .tauc-chip.success {{
        background: var(--tauc-chip-success);
        color: #10b981;
    }}

    .tauc-chip.error {{
        background: var(--tauc-chip-error);
        color: #f87171;
    }}

    .stDataFrame {{
        border-radius: 18px;
        border: 1px solid var(--tauc-border-soft);
        overflow: hidden;
        box-shadow: var(--tauc-shadow);
        background: var(--tauc-bg-card);
    }}

    .stDataFrame [data-testid="StyledDataFrame"] > div:first-child {{
        border-bottom: 1px solid var(--tauc-border);
    }}

    .stDataFrame [data-testid="StyledDataFrame"] > div {{
        background: var(--tauc-bg-card);
    }}

    .stDataFrame tbody tr {{
        transition: background 0.2s ease;
        background: var(--tauc-table-row-bg);
    }}

    .stDataFrame tbody tr:nth-child(even) {{
        background: var(--tauc-table-row-even);
    }}

    .stDataFrame tbody tr:hover {{
        background: var(--tauc-table-hover);
    }}

    .stDataFrame th {{
        background: var(--tauc-table-header) !important;
        color: var(--tauc-table-text) !important;
        font-weight: 600 !important;
        border-bottom: none !important;
    }}

    .stDataFrame td {{
        color: var(--tauc-table-text) !important;
        border-bottom: 1px solid rgba(99, 123, 155, 0.12) !important;
        background: transparent !important;
    }}

    .stDataFrame table {{
        background: transparent !important;
        color: var(--tauc-table-text) !important;
    }}

    /* EXPANDER - All states */
    .streamlit-expanderHeader,
    details summary,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] > div > div {{
        font-weight: 600 !important;
        color: var(--tauc-text-primary) !important;
        border: 1px solid var(--tauc-border) !important;
        border-radius: 12px !important;
        background: var(--tauc-bg-card) !important;
        padding: 0.75rem 1rem !important;
    }}

    /* EXPANDER - Hover state */
    .streamlit-expanderHeader:hover,
    details summary:hover,
    [data-testid="stExpander"] summary:hover,
    [data-testid="stExpander"] > div > div:hover {{
        background: var(--tauc-bg-hover) !important;
        border-color: var(--tauc-primary) !important;
    }}

    /* EXPANDER - Open/Active state */
    .streamlit-expanderHeader[aria-expanded="true"],
    details[open] summary,
    [data-testid="stExpander"][aria-expanded="true"] summary,
    [data-testid="stExpander"][aria-expanded="true"] > div > div {{
        background: var(--tauc-bg-card) !important;
        color: var(--tauc-text-primary) !important;
        border-color: var(--tauc-primary) !important;
    }}

    /* EXPANDER - Content area */
    .streamlit-expanderContent,
    details > div,
    [data-testid="stExpander"] > div > div > div {{
        background: var(--tauc-bg-card) !important;
        border-radius: 0 0 12px 12px !important;
        color: var(--tauc-text-secondary) !important;
        padding: 1rem !important;
    }}

    /* EXPANDER - SVG icons */
    .streamlit-expanderHeader svg,
    [data-testid="stExpander"] svg {{
        color: var(--tauc-text-primary) !important;
        fill: var(--tauc-text-primary) !important;
    }}

    /* EXPANDER - Additional catch-all selectors */
    [class*="expander"] {{
        background: var(--tauc-bg-card) !important;
        color: var(--tauc-text-primary) !important;
    }}

    [class*="expanderHeader"] {{
        background: var(--tauc-bg-card) !important;
        color: var(--tauc-text-primary) !important;
        border: 1px solid var(--tauc-border) !important;
    }}

    [class*="expanderContent"] {{
        background: var(--tauc-bg-card) !important;
        color: var(--tauc-text-secondary) !important;
    }}

    .tauc-notification {{
        display: flex;
        flex-direction: column;
        gap: 0.45rem;
        background: linear-gradient(140deg, var(--tauc-notification-start) 0%, var(--tauc-notification-end) 100%);
        border-radius: 18px;
        padding: 1rem 1.2rem;
        border: 1px solid var(--tauc-border-soft);
        box-shadow: var(--tauc-shadow-soft);
    }}

    div[data-testid="stCodeBlock"] pre {{
        background: var(--tauc-code-bg) !important;
        border-radius: 14px !important;
        border: 1px solid var(--tauc-code-border) !important;
        color: var(--tauc-code-text) !important;
        box-shadow: var(--tauc-shadow-soft);
    }}

    div[data-testid="stCodeBlock"] pre code {{
        color: inherit !important;
        background: transparent !important;
    }}

    span[data-testid="stCaption"] {{
        color: var(--tauc-text-muted) !important;
    }}

    div[data-testid="stMarkdownContainer"] {{
        color: var(--tauc-text-secondary);
    }}

    .stMarkdown ul li::marker {{
        color: var(--tauc-primary);
    }}

    ::selection {{
        background: rgba(14, 165, 233, 0.35);
        color: #0f172a;
    }}

    body.dark-mode ::selection {{
        background: rgba(0, 188, 212, 0.4);
        color: #f7fbff;
    }}

    div[data-testid="stSpinner"] > div {{
        color: var(--tauc-text-secondary) !important;
    }}

    .tauc-notification__title {{
        font-weight: 600;
        color: var(--tauc-text-primary);
        font-size: 0.95rem;
    }}

    .tauc-notification__meta {{
        color: var(--tauc-text-muted);
        font-size: 0.74rem;
    }}

    .status-online {{ color: #10b981; }}
    .status-offline {{ color: #f97316; }}
    .status-outage {{ color: #f87171; }}

    .tauc-divider {{
        border-bottom: 1px solid var(--tauc-border) !important;
        margin: 1.8rem 0 1.2rem !important;
    }}

    /* HR elements - ALL contexts */
    hr,
    .stMarkdown hr,
    div[data-testid="stMarkdownContainer"] hr,
    .stForm hr,
    [class*="markdown"] hr {{
        border: none !important;
        border-top: 1px solid var(--tauc-border) !important;
        margin: 1.5rem 0 !important;
        opacity: 1 !important;
        height: 0 !important;
        background-color: transparent !important;
        background: none !important;
    }}

    ::-webkit-scrollbar-track {{
        background: {colors['scrollbar_track']};
    }}
</style>
"""

"""Dark-first theme CSS for TracePilot AI dashboard."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --tp-bg: #0a0e17;
    --tp-bg-secondary: #111827;
    --tp-card: rgba(17, 24, 39, 0.72);
    --tp-card-hover: rgba(24, 32, 48, 0.85);
    --tp-border: rgba(148, 163, 184, 0.12);
    --tp-border-strong: rgba(148, 163, 184, 0.22);
    --tp-text: #f1f5f9;
    --tp-text-muted: #94a3b8;
    --tp-accent: #6366f1;
    --tp-accent-soft: rgba(99, 102, 241, 0.15);
    --tp-success: #22c55e;
    --tp-warning: #f59e0b;
    --tp-error: #ef4444;
    --tp-info: #38bdf8;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: var(--tp-bg);
    color: var(--tp-text);
}

/* Native Streamlit toolbar: Deploy button, "running man" status widget,
   and the "⋮" menu. This is Streamlit's own chrome (distinct from our
   app's Refresh/Settings buttons, styled separately below) and keeps
   its default white background unless themed explicitly, which makes
   its icons/text invisible once our global light text color applies. */
header[data-testid="stHeader"] {
    background: var(--tp-bg) !important;
    border-bottom: 1px solid var(--tp-border);
}

header[data-testid="stHeader"] * {
    color: var(--tp-text) !important;
    fill: var(--tp-text) !important;
}

header[data-testid="stHeader"] button,
header[data-testid="stHeader"] [role="button"],
header[data-testid="stHeader"] [data-testid^="stBaseButton"],
header[data-testid="stHeader"] [data-testid="stStatusWidget"] {
    background: var(--tp-card) !important;
    border: 1px solid var(--tp-border) !important;
    border-radius: 8px !important;
}

header[data-testid="stHeader"] button:hover,
header[data-testid="stHeader"] [role="button"]:hover,
header[data-testid="stHeader"] [data-testid^="stBaseButton"]:hover {
    background: var(--tp-card-hover) !important;
}

.block-container {
    padding-top: 4.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1321 0%, #0a0e17 100%);
    border-right: 1px solid var(--tp-border);
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--tp-text);
}

div[data-testid="stMetric"] {
    background: var(--tp-card);
    border: 1px solid var(--tp-border);
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(12px);
}

div[data-testid="stMetric"] label {
    color: var(--tp-text-muted) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--tp-text) !important;
    font-weight: 700 !important;
}

.stButton > button {
    background: var(--tp-card) !important;
    border: 1px solid var(--tp-border-strong) !important;
    border-radius: 10px !important;
    color: var(--tp-text) !important;
    font-weight: 500;
}

.stButton > button:hover {
    background: var(--tp-card-hover) !important;
    border-color: var(--tp-accent) !important;
    color: var(--tp-text) !important;
}

.stButton > button p {
    color: var(--tp-text) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600;
    padding: 0.55rem 1.4rem;
    transition: opacity 0.15s ease;
}

.stButton > button[kind="primary"] p {
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    opacity: 0.92;
    border: none !important;
    color: white !important;
}

/* Popover trigger (e.g. "Settings") and its dropdown panel */
[data-testid="stPopover"] > div > button {
    background: var(--tp-card) !important;
    border: 1px solid var(--tp-border-strong) !important;
    border-radius: 10px !important;
    color: var(--tp-text) !important;
}

[data-testid="stPopover"] > div > button:hover {
    background: var(--tp-card-hover) !important;
    border-color: var(--tp-accent) !important;
    color: var(--tp-text) !important;
}

[data-testid="stPopover"] > div > button p {
    color: var(--tp-text) !important;
}

div[data-testid="stPopoverBody"] {
    background: var(--tp-bg-secondary) !important;
    border: 1px solid var(--tp-border-strong) !important;
    color: var(--tp-text) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: var(--tp-bg-secondary) !important;
    border: 1px solid var(--tp-border-strong) !important;
    border-radius: 10px !important;
    color: var(--tp-text) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: var(--tp-card);
    border-radius: 8px;
    border: 1px solid var(--tp-border);
    color: var(--tp-text-muted);
    padding: 8px 16px;
}

.stTabs [aria-selected="true"] {
    background: var(--tp-accent-soft) !important;
    border-color: rgba(99, 102, 241, 0.4) !important;
    color: var(--tp-text) !important;
}

.stDataFrame {
    border: 1px solid var(--tp-border);
    border-radius: 12px;
    overflow: hidden;
}

/* Custom TracePilot components */
.tp-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0 1.5rem 0;
    border-bottom: 1px solid var(--tp-border);
    margin-bottom: 1.75rem;
}

.tp-header-left h1 {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
    color: var(--tp-text);
    letter-spacing: -0.02em;
}

.tp-header-left p {
    margin: 0.25rem 0 0 0;
    color: var(--tp-text-muted);
    font-size: 0.875rem;
}

.tp-header-right {
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
}

.tp-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid var(--tp-border);
    background: var(--tp-card);
    color: var(--tp-text-muted);
}

.tp-badge.online { border-color: rgba(34, 197, 94, 0.35); color: #4ade80; }
.tp-badge.offline { border-color: rgba(239, 68, 68, 0.35); color: #f87171; }
.tp-badge.connected { border-color: rgba(56, 189, 248, 0.35); color: #38bdf8; }

.tp-card {
    background: var(--tp-card);
    border: 1px solid var(--tp-border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(12px);
    margin-bottom: 1rem;
}

.tp-card-title {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--tp-text-muted);
    margin-bottom: 0.5rem;
}

.tp-card-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--tp-text);
    line-height: 1.2;
}

.tp-card-trend {
    font-size: 0.78rem;
    margin-top: 0.35rem;
    color: var(--tp-text-muted);
}

.tp-card-trend.up { color: #4ade80; }
.tp-card-trend.down { color: #f87171; }

.tp-gauge-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem 0;
}

.tp-gauge {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-bottom: 1rem;
}

.tp-gauge-inner {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: var(--tp-bg-secondary);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--tp-border);
}

.tp-gauge-score {
    font-size: 2rem;
    font-weight: 700;
    color: var(--tp-text);
    line-height: 1;
}

.tp-gauge-label {
    font-size: 0.7rem;
    color: var(--tp-text-muted);
    margin-top: 2px;
}

.tp-status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--tp-border);
    font-size: 0.875rem;
}

.tp-status-row:last-child { border-bottom: none; }

.tp-status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}

.tp-status-dot.excellent { background: #22c55e; }
.tp-status-dot.good { background: #84cc16; }
.tp-status-dot.fair { background: #f59e0b; }
.tp-status-dot.poor { background: #ef4444; }

.tp-timeline {
    padding: 0.5rem 0 0.5rem 1rem;
    border-left: 2px solid var(--tp-border-strong);
    margin-left: 0.5rem;
}

.tp-timeline-item {
    position: relative;
    padding: 0 0 1.25rem 1.25rem;
}

.tp-timeline-item::before {
    content: '';
    position: absolute;
    left: -1.45rem;
    top: 0.35rem;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--tp-accent);
    border: 2px solid var(--tp-bg);
}

.tp-timeline-item.error::before { background: var(--tp-error); }

.tp-timeline-name {
    font-weight: 600;
    color: var(--tp-text);
    font-size: 0.9rem;
}

.tp-timeline-duration {
    color: var(--tp-text-muted);
    font-size: 0.8rem;
    font-family: 'SF Mono', 'Consolas', monospace;
}

.tp-bottleneck {
    border-left: 3px solid var(--tp-warning);
    padding-left: 1rem;
}

.tp-bottleneck.high { border-left-color: var(--tp-error); }
.tp-bottleneck.medium { border-left-color: var(--tp-warning); }
.tp-bottleneck.low { border-left-color: var(--tp-info); }

.tp-reco-card {
    background: var(--tp-card);
    border: 1px solid var(--tp-border);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}

.tp-reco-card.high { border-left: 3px solid var(--tp-error); }
.tp-reco-card.medium { border-left: 3px solid var(--tp-warning); }
.tp-reco-card.low { border-left: 3px solid var(--tp-info); }

.tp-reco-title {
    font-weight: 600;
    color: var(--tp-text);
    margin-bottom: 0.35rem;
}

.tp-reco-meta {
    font-size: 0.8rem;
    color: var(--tp-text-muted);
}

.tp-empty {
    text-align: center;
    padding: 3rem 2rem;
    background: var(--tp-card);
    border: 1px dashed var(--tp-border-strong);
    border-radius: 14px;
}

.tp-empty h3 {
    color: var(--tp-text);
    margin-bottom: 0.5rem;
}

.tp-empty p {
    color: var(--tp-text-muted);
    margin-bottom: 1.25rem;
}

.tp-answer-card {
    background: var(--tp-bg-secondary);
    border: 1px solid var(--tp-border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    line-height: 1.65;
    color: var(--tp-text);
}

.tp-sidebar-logo {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--tp-text);
    padding: 0.5rem 0 1.5rem 0;
    letter-spacing: -0.02em;
}

.tp-sidebar-logo span {
    color: var(--tp-accent);
}

.tp-sidebar-status {
    margin-top: auto;
    padding-top: 1.5rem;
    border-top: 1px solid var(--tp-border);
    font-size: 0.78rem;
    color: var(--tp-text-muted);
}

.tp-trace-tree {
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 0.82rem;
    background: var(--tp-bg-secondary);
    border: 1px solid var(--tp-border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    color: var(--tp-text-muted);
    line-height: 1.8;
}

.tp-trace-tree .span-name { color: var(--tp-text); font-weight: 500; }
.tp-trace-tree .span-ok { color: #4ade80; }
.tp-trace-tree .span-err { color: #f87171; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

h1, h2, h3, h4, h5, h6, p, label, span {
    color: var(--tp-text);
}

.stAlert > div {
    border-radius: 10px;
}
</style>
"""
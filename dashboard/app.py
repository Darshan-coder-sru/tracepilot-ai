import sys
import os

import streamlit as st
from dotenv import load_dotenv

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

load_dotenv()

from dashboard.ui.components import inject_theme, render_header
from dashboard.ui.helpers import NAV_PAGES, groq_configured, signoz_configured
from dashboard.ui.pages import (
    cost,
    failure,
    health,
    history,
    overview,
    performance,
    recommendations,
    run_agent,
    timeline,
    traces,
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="TracePilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()

# =====================================
# SESSION STATE
# =====================================

if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

if "last_question" not in st.session_state:
    st.session_state["last_question"] = None

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "overview"

if "signoz_status" not in st.session_state:
    st.session_state["signoz_status"] = (
        "connected" if signoz_configured() else "unknown"
    )

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown(
        '<div class="tp-sidebar-logo">🚀 Trace<span>Pilot</span> AI</div>',
        unsafe_allow_html=True,
    )
    st.caption("AI Agent Observability")

    labels = [label for label, _ in NAV_PAGES]
    keys = [key for _, key in NAV_PAGES]
    key_to_label = dict(zip(keys, labels))
    label_to_key = dict(zip(labels, keys))

    current_label = key_to_label.get(
        st.session_state["current_page"], "Overview"
    )
    selected_label = st.radio(
        "Navigation",
        labels,
        index=labels.index(current_label) if current_label in labels else 0,
        label_visibility="collapsed",
    )
    st.session_state["current_page"] = label_to_key[selected_label]

    st.markdown("---")

    agent_online = groq_configured()
    signoz_ok = signoz_configured()

    agent_status = "Online" if agent_online else "Offline"
    agent_class = "online" if agent_online else "offline"
    signoz_status = "Connected" if signoz_ok else "Not Configured"
    signoz_class = "connected" if signoz_ok else "offline"

    st.markdown(
        f"""
        <div class="tp-sidebar-status">
            <div style="margin-bottom:0.5rem;font-weight:600;color:#94a3b8;">
                CONNECTION STATUS
            </div>
            <div style="margin-bottom:0.35rem;">
                <span class="tp-badge {agent_class}">● Agent {agent_status}</span>
            </div>
            <div>
                <span class="tp-badge {signoz_class}">● SigNoz {signoz_status}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================
# HEADER
# =====================================

header_cols = st.columns([6, 1, 1])

with header_cols[0]:
    render_header(
        agent_online=groq_configured(),
        environment=os.getenv("TRACEPILOT_ENV", "Development"),
    )

with header_cols[1]:
    if st.button("Refresh", use_container_width=True):
        st.session_state["cached_traces"] = None
        st.rerun()

with header_cols[2]:
    with st.popover("Settings"):
        st.markdown("**Environment Variables**")
        st.code(
            "GROQ_API_KEY\n"
            "SIGNOZ_ENDPOINT\n"
            "SIGNOZ_INGESTION_KEY\n"
            "SIGNOZ_API_URL\n"
            "SIGNOZ_API_KEY",
            language="text",
        )
        st.caption("Configure these in your `.env` file at the project root.")

# =====================================
# PAGE ROUTER
# =====================================

PAGE_RENDERERS = {
    "overview": overview.render,
    "run_agent": run_agent.render,
    "performance": performance.render,
    "health": health.render,
    "failure": failure.render,
    "recommendations": recommendations.render,
    "cost": cost.render,
    "timeline": timeline.render,
    "traces": traces.render,
    "history": history.render,
}

page = st.session_state["current_page"]
renderer = PAGE_RENDERERS.get(page, overview.render)
renderer()

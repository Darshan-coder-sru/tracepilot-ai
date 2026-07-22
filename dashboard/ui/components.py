"""Reusable Streamlit UI components for TracePilot AI."""

import streamlit as st

from dashboard.ui.helpers import health_color_label, status_class


def inject_theme():
    from dashboard.ui.theme import CUSTOM_CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header(agent_online=True, environment="Development"):
    signoz_ok = st.session_state.get("signoz_status", "unknown") == "connected"
    signoz_label = "Connected" if signoz_ok else "Not Connected"
    signoz_class = "connected" if signoz_ok else "offline"

    agent_label = "Online" if agent_online else "Offline"
    agent_class = "online" if agent_online else "offline"

    st.markdown(
        f"""
        <div class="tp-header">
            <div class="tp-header-left">
                <h1>TracePilot AI</h1>
                <p>AI Agent Observability Platform</p>
            </div>
            <div class="tp-header-right">
                <span class="tp-badge">{environment}</span>
                <span class="tp-badge {agent_class}">● Agent {agent_label}</span>
                <span class="tp-badge {signoz_class}">● SigNoz {signoz_label}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, trend=None, trend_label=""):
    trend_html = ""
    if trend:
        direction, _ = trend
        if direction == "up":
            trend_html = f'<div class="tp-card-trend up">▲ {trend_label}</div>'
        elif direction == "down":
            trend_html = f'<div class="tp-card-trend down">▼ {trend_label}</div>'
        else:
            trend_html = f'<div class="tp-card-trend">— {trend_label}</div>'

    st.markdown(
        f"""
        <div class="tp-card">
            <div class="tp-card-title">{label}</div>
            <div class="tp-card-value">{value}</div>
            {trend_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def health_gauge(score, status_text=None):
    status = status_text or health_color_label(score)
    pct = max(0, min(100, score))
    color = "#22c55e" if score >= 80 else "#f59e0b" if score >= 50 else "#ef4444"

    st.markdown(
        f"""
        <div class="tp-gauge-wrap">
            <div class="tp-gauge" style="background: conic-gradient({color} {pct * 3.6}deg, rgba(148,163,184,0.15) 0deg);">
                <div class="tp-gauge-inner">
                    <div class="tp-gauge-score">{score}</div>
                    <div class="tp-gauge-label">/ 100</div>
                </div>
            </div>
            <div style="font-weight:600;color:#f1f5f9;margin-bottom:4px;">Agent Health</div>
            <div style="color:#94a3b8;font-size:0.875rem;">Status: {status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sub_score_rows(sub_scores):
    rows = ""
    for name, label in sub_scores.items():
        dot_class = status_class(label)
        rows += f"""
        <div class="tp-status-row">
            <span>{name}</span>
            <span><span class="tp-status-dot {dot_class}"></span>{label}</span>
        </div>
        """
    st.markdown(f'<div class="tp-card">{rows}</div>', unsafe_allow_html=True)


def bottleneck_card(bottleneck):
    sev = bottleneck.get("severity", "LOW").lower()
    st.markdown(
        f"""
        <div class="tp-card tp-bottleneck {sev}">
            <div class="tp-card-title">Bottleneck Detected</div>
            <div style="font-weight:600;color:#f1f5f9;margin:0.5rem 0;">
                Component: {bottleneck['component']}
            </div>
            <div class="tp-reco-meta">Latency: {bottleneck['latency']:.2f}s</div>
            <div class="tp-reco-meta">Impact: {bottleneck['severity']}</div>
            <div class="tp-reco-meta" style="margin-top:0.5rem;">
                Recommendation: {bottleneck['suggestion']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(title, message, button_label=None, button_key=None):
    st.markdown(
        f"""
        <div class="tp-empty">
            <h3>{title}</h3>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if button_label and button_key:
        if st.button(button_label, type="primary", key=button_key):
            st.session_state["current_page"] = "run_agent"
            st.rerun()


def no_run_yet(feature_name):
    empty_state(
        "No agent runs yet",
        f"Run your first research task to begin monitoring. {feature_name} will appear after a run.",
        button_label="Run Agent",
        button_key=f"empty_run_{feature_name}",
    )


def render_vertical_timeline(timeline_steps, start_label="Agent Started", end_label="Agent Completed"):
    if not timeline_steps:
        return

    items_html = f"""
    <div class="tp-timeline-item">
        <div class="tp-timeline-name">● {start_label}</div>
    </div>
    """

    for step in timeline_steps:
        err = step.get("status") == "error"
        icon = step.get("icon", "")
        items_html += f"""
        <div class="tp-timeline-item {'error' if err else ''}">
            <div class="tp-timeline-name">{icon} {step['name']}</div>
            <div class="tp-timeline-duration">{step['duration']:.2f}s</div>
        </div>
        """

    items_html += f"""
    <div class="tp-timeline-item">
        <div class="tp-timeline-name">● {end_label}</div>
    </div>
    """

    st.markdown(f'<div class="tp-timeline">{items_html}</div>', unsafe_allow_html=True)


def recommendation_card(rec):
    priority = rec.get("priority", "LOW").lower()
    st.markdown(
        f"""
        <div class="tp-reco-card {priority}">
            <div class="tp-reco-title">{rec.get('icon', '')} {rec.get('area', 'General')}</div>
            <div class="tp-reco-meta"><strong>Reason:</strong> {rec.get('message', '')}</div>
            <div class="tp-reco-meta" style="margin-top:0.35rem;">
                <strong>Priority:</strong> {rec.get('priority', 'LOW')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def failure_card(report, bottleneck_severity="HIGH"):
    st.markdown(
        f"""
        <div class="tp-card" style="border-left:3px solid #ef4444;">
            <div class="tp-card-title">Failure Detected</div>
            <div style="font-weight:600;color:#f87171;margin:0.5rem 0;">
                {report.get('icon', '')} {report.get('category', 'Unknown')}
            </div>
            <div class="tp-reco-meta"><strong>Error:</strong> {report.get('error_text', '')}</div>
            <div class="tp-reco-meta"><strong>Root Cause:</strong> {report.get('root_cause', '')}</div>
            <div class="tp-reco-meta"><strong>Suggested Solution:</strong> {report.get('fix', '')}</div>
            <div class="tp-reco-meta" style="margin-top:0.5rem;">
                <strong>Severity:</strong> {bottleneck_severity}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def answer_card(text, is_error=False):
    border = "#ef4444" if is_error else "var(--tp-border)"
    st.markdown(
        f'<div class="tp-answer-card" style="border-color:{border};">{text}</div>',
        unsafe_allow_html=True,
    )


def trace_tree_html(result):
    """Build a visual span tree from last run data (local approximation)."""
    if not result:
        return ""

    err = result.get("error", False)
    status_cls = "span-err" if err else "span-ok"
    bn = result.get("bottleneck", {})

    return f"""
    <div class="tp-trace-tree">
        <div><span class="span-name">research_agent</span> <span class="{status_cls}">{'ERROR' if err else 'OK'}</span> — {result.get('total_latency', 0):.2f}s</div>
        <div style="padding-left:1rem;">├── <span class="span-name">planning</span> <span class="span-ok">OK</span></div>
        <div style="padding-left:1rem;">├── <span class="span-name">web_search</span> <span class="span-ok">OK</span> — {result.get('search_latency', 0):.2f}s</div>
        <div style="padding-left:1rem;">├── <span class="span-name">llm_analysis</span> <span class="{status_cls}">{'ERROR' if err else 'OK'}</span> — {result.get('llm_latency', 0):.2f}s</div>
        <div style="padding-left:1rem;">└── <span class="span-name">metrics</span> health={result.get('health_score', 'N/A')} bottleneck={bn.get('component', 'N/A')}</div>
    </div>
    """

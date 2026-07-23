"""Health Score page."""

import streamlit as st

from dashboard.ui.components import health_gauge, no_run_yet, render_html, sub_score_rows


def render():
    st.markdown("### Health Score")
    st.caption("Composite agent health based on latency, errors, and token usage.")

    result = st.session_state.get("last_result")

    if not result:
        no_run_yet("Health score")
        return

    col_gauge, col_details = st.columns([1, 1])

    with col_gauge:
        health_gauge(result["health_score"], result.get("health_status", ""))

    with col_details:
        from dashboard.ui.helpers import derive_sub_scores

        sub_score_rows(derive_sub_scores(result))

        st.markdown("")
        bn = result.get("bottleneck", {})
        render_html(
            f"""
            <div class="tp-card">
                <div class="tp-card-title">Grade</div>
                <div class="tp-card-value">{result.get('health_grade', 'N/A')}</div>
                <div class="tp-reco-meta" style="margin-top:0.5rem;color:#94a3b8;">
                    Bottleneck: {bn.get('component', 'N/A')} ({bn.get('latency', 0):.2f}s)
                </div>
                <div class="tp-reco-meta" style="color:#94a3b8;">{bn.get('message', '')}</div>
            </div>
            """
        )
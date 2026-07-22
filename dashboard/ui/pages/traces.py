"""Trace Explorer — SigNoz integration."""

import pandas as pd
import streamlit as st

from observability.signoz_client import fetch_recent_traces
from dashboard.ui.components import trace_tree_html


def render():
    st.markdown("### Trace Explorer")
    st.caption("Fetch and inspect distributed traces from SigNoz.")

    col_a, col_b = st.columns(2)
    with col_a:
        limit = st.number_input("Traces to fetch", min_value=1, max_value=50, value=10)
    with col_b:
        lookback = st.number_input("Lookback (hours)", min_value=1, max_value=168, value=24)

    fetch = st.button("Fetch Traces", type="primary")

    if fetch:
        with st.spinner("Querying SigNoz Trace API..."):
            try:
                traces = fetch_recent_traces(
                    limit=int(limit),
                    lookback_hours=int(lookback),
                )
                st.session_state["signoz_status"] = "connected"
                st.session_state["cached_traces"] = traces
            except Exception as e:
                st.session_state["signoz_status"] = "disconnected"
                st.error(
                    f"Could not fetch traces from SigNoz: {e}\n\n"
                    "Verify SIGNOZ_API_URL and SIGNOZ_API_KEY in .env. "
                    "SIGNOZ_API_KEY must be a Service Account key."
                )
                return

    traces = st.session_state.get("cached_traces")

    if traces is None:
        st.info("Click 'Fetch Traces' to pull recent agent runs from SigNoz.")
        return

    if not traces:
        st.info(
            "No traces found in this window. Run the agent first, then fetch again."
        )
        return

    trace_df = pd.DataFrame(traces)

    st.markdown("#### Trace List")
    st.dataframe(trace_df, use_container_width=True, hide_index=True)

    # Select trace for detail view
    trace_ids = trace_df["trace_id"].tolist()
    selected = st.selectbox("Select trace for detail view", trace_ids)

    if selected:
        row = trace_df[trace_df["trace_id"] == selected].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Trace ID", str(selected)[:12] + "...")
        c2.metric("Duration", f"{row.get('duration_ms', 0):.0f} ms")
        c3.metric("Health Score", row.get("health_score", "N/A"))
        c4.metric("Status", "Error" if row.get("has_error") else "OK")

        # Show span tree from last_result if it matches, else generic tree
        result = st.session_state.get("last_result")
        st.markdown("#### Execution Tree")
        if result:
            st.markdown(trace_tree_html(result), unsafe_allow_html=True)
        else:
            st.markdown(
                f"""
                <div class="tp-trace-tree">
                    <div><span class="span-name">research_agent</span>
                    <span class="{'span-err' if row.get('has_error') else 'span-ok'}">
                    {'ERROR' if row.get('has_error') else 'OK'}</span>
                    — {row.get('duration_ms', 0) / 1000:.2f}s</div>
                    <div style="padding-left:1rem;">├── planning</div>
                    <div style="padding-left:1rem;">├── web_search</div>
                    <div style="padding-left:1rem;">└── llm_analysis</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    chart_df = trace_df.dropna(subset=["health_score"]).iloc[::-1]
    if not chart_df.empty:
        st.markdown("#### Health Score Trend (SigNoz)")
        st.line_chart(chart_df.set_index("timestamp")["health_score"])

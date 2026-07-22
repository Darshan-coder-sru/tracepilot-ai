"""Run History page — local SQLite log with filters."""

import pandas as pd
import streamlit as st

from dashboard.db import get_run_history
from dashboard.ui.components import empty_state


def render():
    st.markdown("### Run History")
    st.caption("Every agent run logged locally to tracepilot.db — works offline.")

    hist_limit = st.slider("Max runs to load", 5, 100, 30)

    history = get_run_history(limit=hist_limit)

    if not history:
        empty_state(
            "No runs logged yet",
            "Run your first research task to begin building history.",
            button_label="Run Agent",
            button_key="history_empty_run",
        )
        return

    hist_df = pd.DataFrame(history)

    # Filters
    st.markdown("#### Filters")
    fc1, fc2, fc3, fc4 = st.columns(4)

    with fc1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Success", "Failed"],
        )
    with fc2:
        min_health = st.slider("Min Health Score", 0, 100, 0)
    with fc3:
        max_latency = st.slider("Max Latency (s)", 0.0, 60.0, 60.0, 0.5)
    with fc4:
        date_filter = st.text_input("Date contains (YYYY-MM-DD)", placeholder="Optional")

    filtered = hist_df.copy()

    if status_filter == "Success":
        filtered = filtered[filtered["error"] == 0]
    elif status_filter == "Failed":
        filtered = filtered[filtered["error"] == 1]

    if "health_score" in filtered.columns:
        filtered = filtered[
            filtered["health_score"].isna() | (filtered["health_score"] >= min_health)
        ]

    if "total_latency" in filtered.columns:
        filtered = filtered[
            filtered["total_latency"].isna() | (filtered["total_latency"] <= max_latency)
        ]

    if date_filter.strip() and "timestamp" in filtered.columns:
        filtered = filtered[
            filtered["timestamp"].astype(str).str.contains(date_filter.strip())
        ]

    display = filtered[
        [
            "id",
            "timestamp",
            "question",
            "health_score",
            "total_latency",
            "total_tokens",
            "total_cost_usd",
            "error",
        ]
    ].rename(
        columns={
            "id": "Run ID",
            "timestamp": "Timestamp",
            "question": "Question",
            "health_score": "Health",
            "total_latency": "Latency (s)",
            "total_tokens": "Tokens",
            "total_cost_usd": "Cost ($)",
            "error": "Status",
        }
    )

    display["Status"] = display["Status"].map({0: "Success", 1: "Failed"})
    display["Cost ($)"] = display["Cost ($)"].apply(
        lambda x: f"${x:.6f}" if pd.notna(x) else "N/A"
    )
    display["Latency (s)"] = display["Latency (s)"].apply(
        lambda x: f"{x:.2f}" if pd.notna(x) else "N/A"
    )

    st.dataframe(display, use_container_width=True, hide_index=True)

    # Run detail drill-down
    run_ids = filtered["id"].tolist() if not filtered.empty else []
    if run_ids:
        selected_id = st.selectbox("Select run for details", run_ids)
        row = filtered[filtered["id"] == selected_id].iloc[0]

        st.markdown("#### Run Details")
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Health Score", f"{row.get('health_score', 'N/A')}/100")
        d2.metric("Latency", f"{row.get('total_latency', 0):.2f}s")
        d3.metric("Tokens", row.get("total_tokens") or "N/A")
        d4.metric("Status", "Failed" if row.get("error") else "Success")

        st.markdown(f"**Question:** {row.get('question', '')}")
        if row.get("answer"):
            with st.expander("Answer"):
                st.write(row["answer"])

        if row.get("bottleneck_component"):
            st.caption(
                f"Bottleneck: {row['bottleneck_component']} — "
                f"{row.get('bottleneck_message', '')}"
            )

    # Charts
    chart_df = hist_df.dropna(subset=["health_score"]).iloc[::-1]
    if not chart_df.empty:
        st.markdown("#### Health Score Over Time")
        st.line_chart(chart_df.set_index("timestamp")["health_score"])

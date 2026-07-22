"""Execution Timeline page."""

import streamlit as st

from dashboard.ui.components import no_run_yet, render_vertical_timeline


def render():
    st.markdown("### Execution Timeline")
    st.caption("Step-by-step view of the agent pipeline for the most recent run.")

    result = st.session_state.get("last_result")

    if not result:
        no_run_yet("Execution timeline")
        return

    timeline = result.get("timeline") or []

    if not timeline:
        st.info("No timeline data available for the last run.")
        return

    total = result.get("total_latency", 0)
    status_label = "Failed" if result.get("error") else "Completed"

    c1, c2, c3 = st.columns(3)
    c1.metric("Duration", f"{total:.2f}s")
    c2.metric("Steps", len(timeline))
    c3.metric("Status", status_label)

    st.markdown("")
    render_vertical_timeline(timeline)

    # Also show tabular detail
    with st.expander("Detailed step data"):
        import pandas as pd

        df = pd.DataFrame(timeline)
        df["Status"] = df["status"].map({"ok": "OK", "error": "ERROR"})
        display = df[["icon", "name", "start", "end", "duration", "Status"]].rename(
            columns={
                "icon": "",
                "name": "Step",
                "start": "Start (s)",
                "end": "End (s)",
                "duration": "Duration (s)",
            }
        )
        for col in ["Start (s)", "End (s)", "Duration (s)"]:
            display[col] = display[col].round(2)
        st.dataframe(display, use_container_width=True, hide_index=True)

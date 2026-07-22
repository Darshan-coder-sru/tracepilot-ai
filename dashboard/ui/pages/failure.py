"""Failure Analysis page."""

import pandas as pd
import streamlit as st

from dashboard.db import get_run_history
from dashboard.ui.components import failure_card, no_run_yet


def render():
    st.markdown("### Failure Analysis")
    st.caption("Root-cause analysis and error tracking across agent runs.")

    result = st.session_state.get("last_result")

    if not result:
        no_run_yet("Failure analysis")
    elif not result.get("error") or not result.get("failure_report"):
        st.markdown(
            """
            <div class="tp-card" style="border-left:3px solid #22c55e;text-align:center;padding:2rem;">
                <div style="font-size:1.25rem;font-weight:600;color:#4ade80;">No Failures Detected</div>
                <div style="color:#94a3b8;margin-top:0.5rem;">The last run completed successfully.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        report = result["failure_report"]
        sev = result.get("bottleneck", {}).get("severity", "HIGH")
        failure_card(report, bottleneck_severity=sev)

        if report.get("traceback"):
            with st.expander("Show full traceback"):
                st.code(report["traceback"], language="python")

    st.divider()
    st.markdown("#### Error Rate (Last 50 Runs)")

    history = get_run_history(limit=50)
    if history:
        hist_df = pd.DataFrame(history)
        total = len(hist_df)
        errors = int(hist_df["error"].sum())
        rate = (errors / total * 100) if total else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Runs", total)
        c2.metric("Errors", errors)
        c3.metric("Error Rate", f"{rate:.0f}%")

        failed = hist_df[hist_df["error"] == 1]
        if not failed.empty:
            st.markdown("#### Recent Failures")
            st.dataframe(
                failed[["timestamp", "question", "bottleneck_component"]].rename(
                    columns={
                        "timestamp": "Timestamp",
                        "question": "Question",
                        "bottleneck_component": "Component",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.info("No run history available yet.")

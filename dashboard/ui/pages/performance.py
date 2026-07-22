"""Performance analysis page."""

import pandas as pd
import streamlit as st

from dashboard.ui.components import bottleneck_card, no_run_yet


def render():
    st.markdown("### Performance Analysis")
    st.caption("Latency breakdown and bottleneck detection for the most recent run.")

    result = st.session_state.get("last_result")

    if not result:
        no_run_yet("Performance analysis")
        return

    # Latency metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Latency", f"{result['total_latency']:.2f}s")
    c2.metric("Search Latency", f"{result['search_latency']:.2f}s")
    c3.metric("LLM Latency", f"{result['llm_latency']:.2f}s")
    processing = max(
        0,
        result["total_latency"] - result["search_latency"] - result["llm_latency"],
    )
    c4.metric("Processing", f"{processing:.2f}s")

    st.markdown("")

    col_chart, col_bn = st.columns([2, 1])

    with col_chart:
        st.markdown("#### Latency Breakdown")
        perf_df = pd.DataFrame(
            {
                "Stage": ["Web Search", "LLM Analysis", "Processing", "Total"],
                "Seconds": [
                    result["search_latency"],
                    result["llm_latency"],
                    processing,
                    result["total_latency"],
                ],
            }
        ).set_index("Stage")
        st.bar_chart(perf_df)

    with col_bn:
        if result.get("bottleneck"):
            bottleneck_card(result["bottleneck"])

    # Historical performance from DB
    from dashboard.db import get_run_history

    history = get_run_history(limit=30)
    if history:
        hist_df = pd.DataFrame(history).iloc[::-1]
        if not hist_df.empty:
            st.markdown("#### Historical Latency")
            lat_cols = hist_df[["timestamp", "search_latency", "llm_latency", "total_latency"]].dropna()
            if not lat_cols.empty:
                st.line_chart(
                    lat_cols.set_index("timestamp")[
                        ["search_latency", "llm_latency", "total_latency"]
                    ]
                )

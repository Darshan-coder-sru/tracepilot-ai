"""Overview dashboard — aggregates from local run history."""

import streamlit as st

from dashboard.db import get_run_history
from dashboard.ui.components import health_gauge, metric_card, sub_score_rows
from dashboard.ui.helpers import (
    compute_history_stats,
    derive_sub_scores,
    format_tokens,
    health_color_label,
)


def render():
    st.markdown("### Overview")
    st.caption("Real-time summary of agent execution metrics across all logged runs.")

    history = get_run_history(limit=100)
    stats = compute_history_stats(history)
    result = st.session_state.get("last_result")

    # Top metric cards
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    health_trend = stats.get("health_trend")
    health_trend_lbl = (
        f"{abs(health_trend[1]):.0f} vs prev" if health_trend else ""
    )

    with c1:
        metric_card(
            "Total Runs",
            stats["total_runs"],
            trend=None,
            trend_label="All logged runs",
        )

    with c2:
        avg_h = stats["avg_health"]
        val = f"{avg_h:.0f}/100" if avg_h is not None else "N/A"
        metric_card(
            "Average Health Score",
            val,
            trend=health_trend,
            trend_label=health_trend_lbl,
        )

    with c3:
        avg_l = stats["avg_latency"]
        val = f"{avg_l:.2f}s" if avg_l is not None else "N/A"
        lat_trend = stats.get("latency_trend")
        lat_lbl = f"{abs(lat_trend[1]):.2f}s vs prev" if lat_trend else ""
        metric_card("Average Latency", val, trend=lat_trend, trend_label=lat_lbl)

    with c4:
        metric_card("Total Token Usage", format_tokens(stats["total_tokens"]))

    with c5:
        metric_card("Estimated Cost", f"${stats['total_cost']:.2f}")

    with c6:
        metric_card("Failed Runs", stats["failed_runs"])

    st.markdown("")

    # Health score + sub metrics
    col_left, col_right = st.columns([1, 1])

    with col_left:
        if result:
            health_gauge(result["health_score"], result.get("health_status", ""))
        elif avg_h is not None:
            health_gauge(int(avg_h), health_color_label(int(avg_h)))
        else:
            st.info("Run the agent to see health score details.")

    with col_right:
        if result:
            sub_score_rows(derive_sub_scores(result))
        elif history:
            st.markdown(
                '<div class="tp-card"><div class="tp-card-title">Latest Run Health</div>'
                f'<div class="tp-card-value">{history[0].get("health_score", "N/A")}/100</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.info("Health sub-metrics appear after your first run.")

    # Recent activity chart
    if history:
        import pandas as pd

        hist_df = pd.DataFrame(history).iloc[::-1]
        if not hist_df.empty and "health_score" in hist_df.columns:
            chart_df = hist_df.dropna(subset=["health_score"])
            if not chart_df.empty:
                st.markdown("#### Health Score Trend")
                st.line_chart(chart_df.set_index("timestamp")["health_score"])

        if not hist_df.empty and "total_latency" in hist_df.columns:
            lat_df = hist_df.dropna(subset=["total_latency"])
            if not lat_df.empty:
                st.markdown("#### Latency Trend")
                st.line_chart(lat_df.set_index("timestamp")["total_latency"])

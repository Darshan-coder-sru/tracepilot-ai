"""Token & Cost monitoring page."""

import pandas as pd
import streamlit as st

from dashboard.db import get_run_history
from dashboard.ui.components import no_run_yet


def render():
    st.markdown("### Token & Cost")
    st.caption("Token usage and estimated API cost per run.")

    result = st.session_state.get("last_result")
    history = get_run_history(limit=50)

    # Last run metrics
    if not result:
        no_run_yet("Token and cost tracking")
    elif not result.get("cost_data"):
        st.info("No cost data for the last run (LLM call may not have completed).")
    else:
        cost = result["cost_data"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Prompt Tokens", f"{cost['prompt_tokens']:,}")
        c2.metric("Completion Tokens", f"{cost['completion_tokens']:,}")
        c3.metric("Total Tokens", f"{cost['total_tokens']:,}")
        c4.metric("Estimated Cost", f"${cost['total_cost_usd']:.6f}")

        st.markdown("#### Cost Breakdown")
        breakdown = pd.DataFrame(
            {
                "Type": ["Input Cost", "Output Cost"],
                "USD": [cost["input_cost_usd"], cost["output_cost_usd"]],
            }
        ).set_index("Type")
        st.bar_chart(breakdown)
        st.caption(f"Model: {cost['model']}")

    # Historical trends from DB
    if history:
        hist_df = pd.DataFrame(history)
        token_df = hist_df.dropna(subset=["total_tokens"]).iloc[::-1]
        cost_df = hist_df.dropna(subset=["total_cost_usd"]).iloc[::-1]

        if not token_df.empty:
            st.markdown("#### Token Usage Trend")
            st.line_chart(token_df.set_index("timestamp")["total_tokens"])

        if not cost_df.empty:
            st.markdown("#### Cost Per Run")
            st.line_chart(cost_df.set_index("timestamp")["total_cost_usd"])

        valid = hist_df.dropna(subset=["total_cost_usd"])
        if not valid.empty:
            c1, c2 = st.columns(2)
            max_idx = valid["total_cost_usd"].idxmax()
            most_exp = valid.loc[max_idx]
            c1.metric(
                "Most Expensive Run",
                f"${most_exp['total_cost_usd']:.6f}",
            )
            c2.metric(
                "Average Cost Per Run",
                f"${valid['total_cost_usd'].mean():.6f}",
            )

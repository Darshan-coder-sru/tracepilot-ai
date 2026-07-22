"""AI Recommendations page."""

import streamlit as st

from dashboard.ui.components import no_run_yet, recommendation_card


def render():
    st.markdown("### AI Recommendations")
    st.caption("Actionable optimization suggestions based on the latest agent run.")

    result = st.session_state.get("last_result")

    if not result:
        no_run_yet("Recommendations")
        return

    recs = result.get("recommendations") or []

    if not recs:
        st.info("No recommendations for the last run.")
        return

    for rec in recs:
        recommendation_card(rec)

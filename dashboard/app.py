import sys
import os

import pandas as pd
import streamlit as st

# Make sure the project root is on the path so "agent", "dashboard",
# and "observability" can all be imported regardless of where
# Streamlit is launched from.
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from agent.research_agent import research_agent
from observability.signoz_client import fetch_recent_traces
from dashboard.db import get_run_history


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="TracePilot AI",
    page_icon="🛰️",
    layout="centered"
)

st.title("🛰️ TracePilot AI")
st.caption(
    "Real-time observability for AI agents — powered by OpenTelemetry + SigNoz"
)


# =====================================
# HELPERS
# =====================================

def health_color(score):
    """Return an emoji + color band for a given health score."""
    if score >= 80:
        return "🟢", "green"
    elif score >= 50:
        return "🟡", "orange"
    else:
        return "🔴", "red"


# =====================================
# TABS
# =====================================

run_tab, trace_tab, history_tab = st.tabs(["🚀 Run Agent", "📈 Trace View", "📜 History"])


# =====================================
# TAB 1: RUN AGENT
# =====================================

with run_tab:

    question = st.text_input(
        "Ask your research question",
        placeholder="e.g. Find me the best laptop for AI development"
    )

    run_clicked = st.button("🚀 Run Agent", type="primary")

    if run_clicked:

        if not question.strip():
            st.warning("Please enter a question first.")

        else:
            status = st.status(
                "🤖 Agent is working...",
                expanded=True
            )

            status.write("🧠 Planning research...")
            status.write("🔍 Searching the web...")
            status.write("⚡ Asking the LLM...")

            try:
                result = research_agent(question)
            except Exception as e:
                status.update(
                    label="❌ Agent failed",
                    state="error"
                )
                st.error(f"Something went wrong: {e}")
                st.stop()

            status.update(
                label="✅ Done",
                state="complete",
                expanded=False
            )

            # =====================================
            # FINAL ANSWER
            # =====================================

            st.subheader("📄 Final Answer")

            if result["error"]:
                st.error(result["answer"])
            else:
                st.write(result["answer"])

            # =====================================
            # HEALTH SCORE
            # =====================================

            st.subheader("🩺 Agent Health Score")

            emoji, color = health_color(result["health_score"])

            grade_colors = {
                "A": "green", "B": "green",
                "C": "orange", "D": "orange",
                "F": "red"
            }
            grade_color = grade_colors.get(result["health_grade"], "gray")

            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric(
                    label="Health Score",
                    value=f"{result['health_score']}/100"
                )
                st.markdown(
                    f"**Grade:** :{grade_color}[{result['health_grade']}] "
                    f"— {result['health_status']}"
                )

            with col2:
                st.markdown(
                    f"### {emoji} :{color}[{result['health_score']}/100]"
                )
                st.write(
                    f"**Bottleneck:** {result['bottleneck']['component']} "
                    f"({result['bottleneck']['latency']:.2f}s) — "
                    f"{result['bottleneck']['message']}"
                )
                st.caption(
                    f"Severity: {result['bottleneck']['severity']} — "
                    f"{result['bottleneck']['suggestion']}"
                )

            # =====================================
            # PERFORMANCE BREAKDOWN
            # =====================================

            st.subheader("⏱️ Performance Breakdown")

            perf_df = pd.DataFrame(
                {
                    "Stage": ["Web Search", "LLM Analysis", "Total"],
                    "Seconds": [
                        result["search_latency"],
                        result["llm_latency"],
                        result["total_latency"],
                    ],
                }
            ).set_index("Stage")

            st.bar_chart(perf_df)

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Time", f"{result['total_latency']:.2f}s")
            c2.metric("Search Time", f"{result['search_latency']:.2f}s")
            c3.metric("LLM Time", f"{result['llm_latency']:.2f}s")

            # =====================================
            # TOKEN & COST TRACKING
            # =====================================

            if result["cost_data"]:
                st.subheader("💰 Token & Cost Tracking")

                cost = result["cost_data"]

                t1, t2, t3, t4 = st.columns(4)
                t1.metric("Prompt Tokens", f"{cost['prompt_tokens']:,}")
                t2.metric("Completion Tokens", f"{cost['completion_tokens']:,}")
                t3.metric("Total Tokens", f"{cost['total_tokens']:,}")
                t4.metric("Total Cost", f"${cost['total_cost_usd']:.6f}")

            # =====================================
            # AI RECOMMENDATIONS
            # =====================================

            if result["recommendations"]:
                st.subheader("💡 AI Recommendations")

                priority_style = {
                    "HIGH": st.error,
                    "MEDIUM": st.warning,
                    "LOW": st.info,
                }

                for rec in result["recommendations"]:
                    render = priority_style.get(rec["priority"], st.info)
                    render(
                        f"{rec['icon']} **[{rec['priority']}] {rec['area']}** — "
                        f"{rec['message']}"
                    )

            # =====================================
            # EXECUTION TIMELINE
            # =====================================

            if result["timeline"]:
                st.subheader("📊 Execution Timeline")

                timeline_df = pd.DataFrame(result["timeline"])
                timeline_df["Status"] = timeline_df["status"].map(
                    {"ok": "✅", "error": "❌"}
                )

                display_timeline = timeline_df[[
                    "icon", "name", "start", "end", "duration", "Status"
                ]].rename(columns={
                    "icon": "",
                    "name": "Step",
                    "start": "Start (s)",
                    "end": "End (s)",
                    "duration": "Duration (s)",
                })

                display_timeline["Start (s)"] = display_timeline["Start (s)"].round(2)
                display_timeline["End (s)"] = display_timeline["End (s)"].round(2)
                display_timeline["Duration (s)"] = display_timeline["Duration (s)"].round(2)

                st.dataframe(
                    display_timeline,
                    use_container_width=True,
                    hide_index=True
                )

            # =====================================
            # SIGNOZ LINK
            # =====================================

            st.divider()
            st.caption(
                "📊 This run's trace is being sent to SigNoz in real time. "
                "Check the 'Trace View' tab above to pull it back into this "
                "dashboard, or view it directly in SigNoz under the "
                "'tracepilot-ai' service."
            )


# =====================================
# TAB 2: TRACE VIEW
# =====================================

with trace_tab:

    st.subheader("📈 Recent Agent Traces (from SigNoz)")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        limit = st.number_input(
            "How many traces to fetch",
            min_value=1,
            max_value=50,
            value=10
        )

    with col_b:
        lookback_hours = st.number_input(
            "Lookback window (hours)",
            min_value=1,
            max_value=168,
            value=24
        )

    fetch_clicked = st.button("🔄 Fetch Traces")

    if fetch_clicked:

        with st.spinner("Querying SigNoz Trace API..."):
            try:
                traces = fetch_recent_traces(
                    limit=int(limit),
                    lookback_hours=int(lookback_hours)
                )
            except Exception as e:
                st.error(
                    f"Couldn't fetch traces from SigNoz: {e}\n\n"
                    "Double check SIGNOZ_API_URL and SIGNOZ_API_KEY in your "
                    ".env — SIGNOZ_API_KEY must be a Service Account key "
                    "(Settings -> Service Accounts), not the ingestion key."
                )
                st.stop()

        if not traces:
            st.info(
                "No traces found in this time window. Run the agent at "
                "least once from the 'Run Agent' tab, then fetch again."
            )

        else:
            trace_df = pd.DataFrame(traces)

            st.dataframe(
                trace_df,
                use_container_width=True,
                hide_index=True
            )

            # Health score trend, oldest -> newest for a readable chart
            chart_df = trace_df.dropna(subset=["health_score"]).iloc[::-1]

            if not chart_df.empty:
                st.subheader("Health Score Trend")
                st.line_chart(
                    chart_df.set_index("timestamp")["health_score"]
                )

    else:
        st.caption(
            "Click 'Fetch Traces' to pull the latest agent runs from SigNoz."
        )


# =====================================
# TAB 3: HISTORY (local SQLite log)
# =====================================

with history_tab:

    st.subheader("📜 Local Run History")
    st.caption(
        "Every agent run is logged locally to tracepilot.db, including "
        "failed runs — this works even if SigNoz is unreachable."
    )

    hist_limit = st.slider(
        "Number of runs to show",
        min_value=5,
        max_value=100,
        value=20
    )

    history = get_run_history(limit=hist_limit)

    if not history:
        st.info("No runs logged yet. Try the 'Run Agent' tab first.")

    else:
        hist_df = pd.DataFrame(history)

        # Friendlier column order and naming for display
        display_df = hist_df[[
            "timestamp", "question", "health_score",
            "total_latency", "search_latency", "llm_latency",
            "bottleneck_component", "error"
        ]].rename(columns={
            "timestamp": "Timestamp",
            "question": "Question",
            "health_score": "Health",
            "total_latency": "Total (s)",
            "search_latency": "Search (s)",
            "llm_latency": "LLM (s)",
            "bottleneck_component": "Bottleneck",
            "error": "Errored",
        })

        display_df["Errored"] = display_df["Errored"].map(
            {1: "❌", 0: "✅"}
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # Health score trend, oldest -> newest
        chart_df = hist_df.dropna(subset=["health_score"]).iloc[::-1]

        if not chart_df.empty:
            st.subheader("Health Score Over Time")
            st.line_chart(
                chart_df.set_index("timestamp")["health_score"]
            )

        # Quick summary stats
        total_runs = len(hist_df)
        error_count = int(hist_df["error"].sum())
        avg_health = hist_df["health_score"].dropna().mean()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Runs Logged", total_runs)
        c2.metric("Errors", error_count)
        c3.metric(
            "Avg Health Score",
            f"{avg_health:.0f}/100" if pd.notna(avg_health) else "N/A"
        )
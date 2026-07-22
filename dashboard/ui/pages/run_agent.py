"""Run Agent page — triggers research_agent and shows live progress."""

import streamlit as st

from agent.research_agent import research_agent
from dashboard.ui.components import answer_card, empty_state


STEPS = [
    ("Planning", "Defining research strategy"),
    ("Web Search", "Fetching live results"),
    ("LLM Analysis", "Generating answer with Groq"),
    ("Health Evaluation", "Computing health score"),
    ("Recommendations", "Generating optimization tips"),
]


def render():
    st.markdown("### Run Agent")
    st.caption("Execute a research task and monitor the full agent pipeline in real time.")

    question = st.text_area(
        "What would you like the AI agent to research?",
        placeholder="e.g. Find me the best laptop for AI development under $1500",
        height=100,
        key="run_question",
    )

    run_clicked = st.button("Run Agent", type="primary", use_container_width=True)

    if run_clicked:
        if not question.strip():
            st.warning("Please enter a research question first.")
        else:
            status = st.status("Agent Execution in Progress", expanded=True)

            for i, (step, desc) in enumerate(STEPS, 1):
                status.write(f"**Step {i}: {step}** — {desc}")

            try:
                result = research_agent(question)
            except Exception as e:
                status.update(label="Agent failed", state="error")
                st.error(f"Something went wrong: {e}")
                st.stop()

            status.update(label="Execution complete", state="complete", expanded=False)

            st.session_state["last_result"] = result
            st.session_state["last_question"] = question
            st.success("Agent run completed. Explore other pages for detailed analytics.")

    result = st.session_state.get("last_result")

    if result:
        st.markdown("#### Final Answer")
        if result["error"]:
            answer_card(result["answer"], is_error=True)
        else:
            answer_card(result["answer"].replace("\n", "<br>"))

        st.caption(
            "This run's trace is being sent to SigNoz via OpenTelemetry. "
            "Check Trace Explorer or Overview for analytics."
        )
    elif not run_clicked:
        empty_state(
            "No agent runs yet",
            "Run your first research task to begin monitoring your AI agent.",
            button_label=None,
        )

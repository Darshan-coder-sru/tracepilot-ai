import os
import time

from groq import Groq
from dotenv import load_dotenv
from duckduckgo_search import DDGS

from observability.telemetry import tracer

from dashboard.health_score import (
    calculate_health_score,
    get_health_grade,
    find_bottleneck
)
from dashboard.failure_analysis import analyze_failure, print_failure_report
from dashboard.token_cost import (
    calculate_token_cost,
    extract_token_usage,
    print_token_report
)
from dashboard.recommendations import generate_recommendations, print_recommendations
from dashboard.timeline import ExecutionTimeline


# Load environment variables
load_dotenv()


# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant"


def web_search(query, timeline):
    """
    Search the web and measure actual search latency.
    """

    search_start_time = time.time()

    with tracer.start_as_current_span("web_search") as search_span:

        search_span.set_attribute("search.query", query)

        print("🔍 Searching the web...")

        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=3)
            for result in search_results:
                results.append(
                    f"Title: {result['title']}\n"
                    f"Content: {result['body']}"
                )

        search_latency = time.time() - search_start_time

        search_span.set_attribute("search.latency_seconds", search_latency)
        search_span.set_attribute("search.results_count", len(results))

        print(
            f"✅ Found {len(results)} results "
            f"in {search_latency:.2f} seconds"
        )

        timeline.record(
            name="Web Search",
            start=search_start_time,
            end=time.time(),
            status="ok",
            icon="🔍"
        )

        return "\n\n".join(results), search_latency


def research_agent(question):
    """
    Main AI Research Agent with full observability dashboard.
    """

    agent_start_time = time.time()
    timeline = ExecutionTimeline()
    error_occurred = False
    failure_report = None
    cost_data = None

    with tracer.start_as_current_span("research_agent") as agent_span:

        agent_span.set_attribute("agent.question", question)

        print(f"\n🤖 Agent received: {question}")

        # =============================================
        # STEP 1: PLANNING
        # =============================================

        planning_start = time.time()

        with tracer.start_as_current_span("planning") as planning_span:
            planning_span.set_attribute("agent.step", "planning")
            print("🧠 Planning research...")
            search_query = question

        timeline.record(
            name="Planning",
            start=planning_start,
            end=time.time(),
            status="ok",
            icon="🧠"
        )

        # =============================================
        # STEP 2: WEB SEARCH
        # =============================================

        try:
            search_results, search_latency = web_search(search_query, timeline)
        except Exception as exc:
            search_latency = time.time() - agent_start_time
            error_occurred = True
            failure_report = analyze_failure(exception=exc)
            print_failure_report(failure_report)
            return None

        # =============================================
        # STEP 3: LLM ANALYSIS
        # =============================================

        llm_start_time = time.time()
        answer = None

        with tracer.start_as_current_span("llm_analysis") as llm_span:

            llm_span.set_attribute("agent.step", "llm_analysis")

            print("⚡ Asking Groq AI...")

            prompt = f"""
Answer the user's question using the research results below.

User Question:
{question}

Research Results:
{search_results}

Give a clear, accurate, and useful answer.
"""

            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful research AI agent."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=700
                )

                answer = response.choices[0].message.content

            except Exception as exc:
                error_occurred = True
                failure_report = analyze_failure(exception=exc)
                print_failure_report(failure_report)

            llm_latency = time.time() - llm_start_time

            llm_span.set_attribute("llm.latency_seconds", llm_latency)
            llm_span.set_attribute("llm.model", MODEL)

            # =============================================
            # STEP 4: TOKEN & COST TRACKING
            # =============================================

            if not error_occurred and response:
                prompt_tokens, completion_tokens = extract_token_usage(response)
                cost_data = calculate_token_cost(
                    model=MODEL,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens
                )
                llm_span.set_attribute("llm.prompt_tokens", prompt_tokens)
                llm_span.set_attribute("llm.completion_tokens", completion_tokens)
                llm_span.set_attribute("llm.total_cost_usd", cost_data["total_cost_usd"])

            timeline.record(
                name="LLM Analysis",
                start=llm_start_time,
                end=time.time(),
                status="error" if error_occurred else "ok",
                icon="⚡"
            )

            print("✅ Answer generated!")

        # =============================================
        # STEP 5: COMPUTE ALL METRICS
        # =============================================

        total_latency = time.time() - agent_start_time

        total_tokens = cost_data["total_tokens"] if cost_data else 0

        health_score = calculate_health_score(
            total_latency=total_latency,
            search_latency=search_latency,
            llm_latency=llm_latency,
            error=error_occurred,
            token_count=total_tokens
        )

        grade, status = get_health_grade(health_score)

        bottleneck = find_bottleneck(
            search_latency=search_latency,
            llm_latency=llm_latency
        )

        recommendations = generate_recommendations(
            health_score=health_score,
            bottleneck=bottleneck,
            total_latency=total_latency,
            search_latency=search_latency,
            llm_latency=llm_latency,
            token_cost_data=cost_data,
            error=error_occurred,
            failure_report=failure_report
        )

        # Store all metrics in SigNoz
        agent_span.set_attribute("agent.total_latency_seconds", total_latency)
        agent_span.set_attribute("agent.health_score", health_score)
        agent_span.set_attribute("agent.health_grade", grade)
        agent_span.set_attribute("agent.bottleneck", bottleneck["component"])
        agent_span.set_attribute("agent.error", error_occurred)

        # =============================================
        # STEP 6: PRINT FULL DASHBOARD
        # =============================================

        print(f"\n⏱️  Total Agent Time  : {total_latency:.2f}s")
        print(f"🔍 Search Time      : {search_latency:.2f}s")
        print(f"⚡ LLM Time         : {llm_latency:.2f}s")

        # Health Score
        print(f"\n🩺 AGENT HEALTH SCORE")
        print("=" * 40)
        print(f"Score  : {health_score}/100")
        print(f"Grade  : {grade}  —  {status}")

        # Bottleneck
        print(f"\n🚨 BOTTLENECK DETECTION")
        print("=" * 40)
        print(f"Component : {bottleneck['component']}")
        print(f"Latency   : {bottleneck['latency']:.2f}s")
        print(f"Severity  : {bottleneck['severity']}")
        print(f"Message   : {bottleneck['message']}")
        print(f"Suggestion: {bottleneck['suggestion']}")

        # Failure analysis (only when an error occurred)
        if error_occurred and failure_report:
            print_failure_report(failure_report)

        # Token & cost
        if cost_data:
            print_token_report(cost_data)

        # AI recommendations
        print_recommendations(recommendations)

        # Execution timeline
        timeline.print_timeline()

        return answer


# =============================================
# PROGRAM ENTRY POINT
# =============================================

if __name__ == "__main__":

    question = input("\n🔍 Ask your research question: ")

    answer = research_agent(question)

    if answer:
        print("\n📄 FINAL ANSWER:")
        print(answer)

"""
Quick smoke-test for all dashboard modules.
No API keys required.
"""

from dashboard.health_score import calculate_health_score, get_health_grade, find_bottleneck
from dashboard.failure_analysis import analyze_failure, print_failure_report
from dashboard.token_cost import calculate_token_cost, print_token_report
from dashboard.recommendations import generate_recommendations, print_recommendations
from dashboard.timeline import ExecutionTimeline
import time


# ── Sample telemetry data ──────────────────────────────────────
total_latency = 8.5
search_latency = 5.5
llm_latency = 2.5
prompt_tokens = 320
completion_tokens = 210


# ── 🩺 Health Score ───────────────────────────────────────────
score = calculate_health_score(
    total_latency=total_latency,
    search_latency=search_latency,
    llm_latency=llm_latency,
    token_count=prompt_tokens + completion_tokens
)
grade, status = get_health_grade(score)

print("\n🩺 AGENT HEALTH SCORE")
print("====================")
print(f"Score : {score}/100")
print(f"Grade : {grade}  —  {status}")


# ── 🚨 Bottleneck Detection ───────────────────────────────────
bottleneck = find_bottleneck(
    search_latency=search_latency,
    llm_latency=llm_latency
)

print("\n🚨 BOTTLENECK DETECTION")
print("====================")
print(f"Component : {bottleneck['component']}")
print(f"Latency   : {bottleneck['latency']} seconds")
print(f"Severity  : {bottleneck['severity']}")
print(f"Message   : {bottleneck['message']}")
print(f"Suggestion: {bottleneck['suggestion']}")


# ── ❌ Intelligent Failure Analysis ───────────────────────────
try:
    raise ConnectionError("Network connection refused. Unable to reach api.groq.com.")
except Exception as exc:
    report = analyze_failure(exception=exc)
    print_failure_report(report)


# ── 💰 Token & Cost Tracking ──────────────────────────────────
cost_data = calculate_token_cost(
    model="llama-3.1-8b-instant",
    prompt_tokens=prompt_tokens,
    completion_tokens=completion_tokens
)
print_token_report(cost_data)


# ── 💡 AI Recommendations ─────────────────────────────────────
recommendations = generate_recommendations(
    health_score=score,
    bottleneck=bottleneck,
    total_latency=total_latency,
    search_latency=search_latency,
    llm_latency=llm_latency,
    token_cost_data=cost_data
)
print_recommendations(recommendations)


# ── 📊 Execution Timeline ─────────────────────────────────────
now = time.time()
tl = ExecutionTimeline()
tl._start_time = now - total_latency
tl.record("Planning",    now - 8.5, now - 8.4, "ok",    "🧠")
tl.record("Web Search",  now - 8.4, now - 2.9, "ok",    "🔍")
tl.record("LLM Analysis",now - 2.9, now - 0.4, "ok",    "⚡")
tl.print_timeline()

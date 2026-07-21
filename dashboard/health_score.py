def calculate_health_score(
    total_latency,
    search_latency,
    llm_latency,
    error=False,
    token_count=0
):
    """
    Calculate the health score of the AI agent (0-100).
    Returns score plus a letter grade and status label.
    """

    score = 100

    # 1. Error penalty
    if error:
        score -= 40

    # 2. Total latency penalty
    if total_latency > 15:
        score -= 30
    elif total_latency > 10:
        score -= 20
    elif total_latency > 5:
        score -= 10

    # 3. Search bottleneck penalty
    if search_latency > llm_latency * 2:
        score -= 10

    # 4. Unusually high token usage penalty
    if token_count > 2000:
        score -= 5

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return score


def get_health_grade(score):
    """
    Convert numeric score to letter grade and status label.
    """
    if score >= 90:
        return "A", "Excellent ✅"
    elif score >= 75:
        return "B", "Good 🟢"
    elif score >= 60:
        return "C", "Fair 🟡"
    elif score >= 40:
        return "D", "Poor 🟠"
    else:
        return "F", "Critical 🔴"


def find_bottleneck(
    search_latency,
    llm_latency
):
    """
    Find the slowest component with severity classification.
    """

    if search_latency > llm_latency:
        ratio = search_latency / max(llm_latency, 0.01)
        severity = "HIGH" if ratio > 3 else "MEDIUM" if ratio > 1.5 else "LOW"
        return {
            "component": "Web Search",
            "latency": search_latency,
            "severity": severity,
            "message": "Web search is the main bottleneck.",
            "suggestion": "Consider caching frequent queries or reducing max_results."
        }

    ratio = llm_latency / max(search_latency, 0.01)
    severity = "HIGH" if ratio > 3 else "MEDIUM" if ratio > 1.5 else "LOW"
    return {
        "component": "LLM Analysis",
        "latency": llm_latency,
        "severity": severity,
        "message": "LLM analysis is the main bottleneck.",
        "suggestion": "Consider reducing max_tokens or switching to a faster model."
    }

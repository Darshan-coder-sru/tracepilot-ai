def generate_recommendations(
    health_score,
    bottleneck,
    total_latency,
    search_latency,
    llm_latency,
    token_cost_data=None,
    error=False,
    failure_report=None
):
    """
    Generate actionable AI recommendations based on agent metrics.
    Returns a list of recommendation dicts with priority and message.
    """

    recommendations = []

    # --- Error / failure recommendations ---
    if error and failure_report:
        recommendations.append({
            "priority": "HIGH",
            "icon": "❌",
            "area": "Reliability",
            "message": failure_report.get("fix", "Investigate the last failure before retrying.")
        })

    # --- Health score recommendations ---
    if health_score < 40:
        recommendations.append({
            "priority": "HIGH",
            "icon": "🩺",
            "area": "Health",
            "message": (
                "Agent health is critical. Check for errors, high latency, "
                "and token usage simultaneously."
            )
        })
    elif health_score < 60:
        recommendations.append({
            "priority": "MEDIUM",
            "icon": "🩺",
            "area": "Health",
            "message": (
                "Agent health is below average. "
                "Focus on the highest-latency component first."
            )
        })

    # --- Latency recommendations ---
    if total_latency > 15:
        recommendations.append({
            "priority": "HIGH",
            "icon": "⏱️",
            "area": "Latency",
            "message": (
                f"Total latency is very high ({total_latency:.1f}s). "
                "Consider running search and LLM steps in parallel."
            )
        })
    elif total_latency > 8:
        recommendations.append({
            "priority": "MEDIUM",
            "icon": "⏱️",
            "area": "Latency",
            "message": (
                f"Total latency of {total_latency:.1f}s is above the 8s target. "
                "Profile each step to find the slowest call."
            )
        })

    # --- Bottleneck recommendations ---
    if bottleneck["component"] == "Web Search" and bottleneck["severity"] in ("HIGH", "MEDIUM"):
        recommendations.append({
            "priority": bottleneck["severity"],
            "icon": "🔍",
            "area": "Search",
            "message": (
                f"Web search took {search_latency:.1f}s — "
                "reduce max_results or add query result caching."
            )
        })
    elif bottleneck["component"] == "LLM Analysis" and bottleneck["severity"] in ("HIGH", "MEDIUM"):
        recommendations.append({
            "priority": bottleneck["severity"],
            "icon": "⚡",
            "area": "LLM",
            "message": (
                f"LLM analysis took {llm_latency:.1f}s — "
                "try lowering max_tokens or switching to a faster model."
            )
        })

    # --- Token / cost recommendations ---
    if token_cost_data:
        total_tokens = token_cost_data.get("total_tokens", 0)
        total_cost = token_cost_data.get("total_cost_usd", 0)

        if total_tokens > 1500:
            recommendations.append({
                "priority": "MEDIUM",
                "icon": "💰",
                "area": "Cost",
                "message": (
                    f"Used {total_tokens:,} tokens (${total_cost:.5f}). "
                    "Shorten the prompt or reduce max_tokens to cut costs."
                )
            })
        elif total_cost > 0:
            recommendations.append({
                "priority": "LOW",
                "icon": "💰",
                "area": "Cost",
                "message": (
                    f"Token cost per run: ${total_cost:.6f} "
                    f"({total_tokens:,} tokens). Looking efficient!"
                )
            })

    # --- All good ---
    if not recommendations:
        recommendations.append({
            "priority": "LOW",
            "icon": "✅",
            "area": "General",
            "message": "Agent is performing well. No immediate actions needed."
        })

    # Sort: HIGH → MEDIUM → LOW
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    recommendations.sort(key=lambda r: priority_order.get(r["priority"], 3))

    return recommendations


def print_recommendations(recommendations):
    """
    Pretty-print AI recommendations to the console.
    """
    print("\n💡 AI RECOMMENDATIONS")
    print("=" * 40)
    for i, rec in enumerate(recommendations, 1):
        priority_label = f"[{rec['priority']}]"
        print(
            f"{i}. {rec['icon']} {priority_label:<8} "
            f"({rec['area']}) {rec['message']}"
        )

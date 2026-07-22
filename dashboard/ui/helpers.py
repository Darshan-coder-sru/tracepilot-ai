"""Shared helpers for dashboard UI — aggregates and derived metrics."""

import os

import pandas as pd


NAV_PAGES = [
    ("Overview", "overview"),
    ("Run Agent", "run_agent"),
    ("Performance", "performance"),
    ("Health Score", "health"),
    ("Failure Analysis", "failure"),
    ("AI Recommendations", "recommendations"),
    ("Token & Cost", "cost"),
    ("Execution Timeline", "timeline"),
    ("Trace Explorer", "traces"),
    ("Run History", "history"),
]


def health_color(score):
    if score >= 80:
        return "excellent"
    if score >= 50:
        return "fair"
    return "poor"


def health_color_label(score):
    if score >= 80:
        return "Excellent"
    if score >= 60:
        return "Good"
    if score >= 40:
        return "Fair"
    return "Poor"


def derive_sub_scores(result):
    """Derive health sub-dimensions from existing result fields."""
    if not result:
        return {}

    total_lat = result.get("total_latency", 0)
    error = result.get("error", False)
    cost = result.get("cost_data") or {}
    tokens = cost.get("total_tokens", 0)

    if total_lat <= 5:
        latency = "Excellent"
    elif total_lat <= 10:
        latency = "Good"
    elif total_lat <= 15:
        latency = "Fair"
    else:
        latency = "Poor"

    reliability = "Poor" if error else "Excellent" if total_lat <= 10 else "Good"

    if not cost:
        cost_eff = "N/A"
    elif tokens <= 800:
        cost_eff = "Excellent"
    elif tokens <= 1500:
        cost_eff = "Good"
    else:
        cost_eff = "Fair"

    error_rate = "Poor" if error else "Excellent"

    return {
        "Latency": latency,
        "Reliability": reliability,
        "Cost Efficiency": cost_eff,
        "Error Rate": error_rate,
    }


def status_class(label):
    mapping = {
        "Excellent": "excellent",
        "Good": "good",
        "Fair": "fair",
        "Poor": "poor",
        "N/A": "fair",
    }
    return mapping.get(label, "fair")


def compute_history_stats(history):
    """Aggregate metrics from run history list of dicts."""
    if not history:
        return {
            "total_runs": 0,
            "failed_runs": 0,
            "avg_health": None,
            "avg_latency": None,
            "total_tokens": 0,
            "total_cost": 0.0,
            "health_trend": None,
            "latency_trend": None,
        }

    df = pd.DataFrame(history)
    total = len(df)
    failed = int(df["error"].sum()) if "error" in df.columns else 0

    avg_health = df["health_score"].dropna().mean() if "health_score" in df.columns else None
    avg_latency = df["total_latency"].dropna().mean() if "total_latency" in df.columns else None

    total_tokens = int(df["total_tokens"].fillna(0).sum()) if "total_tokens" in df.columns else 0
    total_cost = float(df["total_cost_usd"].fillna(0).sum()) if "total_cost_usd" in df.columns else 0.0

    health_trend = _trend(df, "health_score", higher_is_better=True)
    latency_trend = _trend(df, "total_latency", higher_is_better=False)

    return {
        "total_runs": total,
        "failed_runs": failed,
        "avg_health": avg_health,
        "avg_latency": avg_latency,
        "total_tokens": total_tokens,
        "total_cost": total_cost,
        "health_trend": health_trend,
        "latency_trend": latency_trend,
        "df": df,
    }


def _trend(df, column, higher_is_better=True, split=5):
    """Compare recent half vs older half for trend indicator."""
    if column not in df.columns or len(df) < 2:
        return None

    series = df[column].dropna()
    if len(series) < 2:
        return None

    # history is newest-first from db
    recent = series.head(min(split, len(series) // 2 or 1))
    older = series.tail(min(split, len(series) // 2 or 1))

    if older.empty or recent.empty:
        return None

    diff = recent.mean() - older.mean()
    if abs(diff) < 0.5 if column == "health_score" else abs(diff) < 0.1:
        return ("neutral", diff)

    improved = diff > 0 if higher_is_better else diff < 0
    return ("up" if improved else "down", diff)


def signoz_configured():
    return bool(os.getenv("SIGNOZ_API_URL") and os.getenv("SIGNOZ_API_KEY"))


def groq_configured():
    return bool(os.getenv("GROQ_API_KEY"))


def format_tokens(n):
    if n is None or pd.isna(n):
        return "0"
    n = int(n)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def severity_from_bottleneck(severity):
    return severity.lower() if severity else "low"

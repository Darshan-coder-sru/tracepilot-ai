import traceback


# Known failure patterns and their diagnoses
FAILURE_PATTERNS = {
    "timeout": {
        "keywords": ["timeout", "timed out", "time out"],
        "category": "Timeout",
        "icon": "⏱️",
        "root_cause": "A component exceeded its allowed response time.",
        "fix": "Increase timeout limits or reduce the scope of the request."
    },
    "rate_limit": {
        "keywords": ["rate limit", "429", "too many requests", "quota"],
        "category": "Rate Limit",
        "icon": "🚦",
        "root_cause": "API rate limit reached for the current tier.",
        "fix": "Add retry logic with exponential backoff, or upgrade your API plan."
    },
    "api_key": {
        "keywords": ["api key", "invalid key", "unauthorized", "401", "authentication"],
        "category": "Authentication",
        "icon": "🔑",
        "root_cause": "API key is missing, invalid, or expired.",
        "fix": "Check that GROQ_API_KEY and SIGNOZ_INGESTION_KEY are set correctly."
    },
    "network": {
        "keywords": ["connection", "network", "dns", "socket", "unreachable", "refused"],
        "category": "Network",
        "icon": "🌐",
        "root_cause": "Cannot reach an external service.",
        "fix": "Check network connectivity and verify the endpoint URL is correct."
    },
    "token_limit": {
        "keywords": ["token", "context length", "max_tokens", "too long"],
        "category": "Token Limit",
        "icon": "📏",
        "root_cause": "Input or output exceeded the model's token limit.",
        "fix": "Reduce max_tokens, shorten the prompt, or use a model with a larger context window."
    },
    "search": {
        "keywords": ["duckduckgo", "search", "ddgs", "no results"],
        "category": "Search Failure",
        "icon": "🔍",
        "root_cause": "Web search returned no results or encountered an error.",
        "fix": "Retry the search, rephrase the query, or add a fallback search provider."
    },
}


def analyze_failure(exception=None, error_message=None):
    """
    Intelligently categorize a failure and provide root cause + fix.

    Pass either an Exception object or a plain error_message string.
    Returns a structured failure report dict.
    """

    if exception is not None:
        error_text = f"{type(exception).__name__}: {str(exception)}"
        tb = traceback.format_exc()
    elif error_message:
        error_text = error_message
        tb = None
    else:
        error_text = "Unknown error"
        tb = None

    error_lower = error_text.lower()

    # Match against known patterns
    matched = None
    for key, pattern in FAILURE_PATTERNS.items():
        if any(kw in error_lower for kw in pattern["keywords"]):
            matched = pattern
            break

    if matched is None:
        matched = {
            "category": "Unknown",
            "icon": "❓",
            "root_cause": "The error did not match any known failure pattern.",
            "fix": "Review the full traceback for more details."
        }

    return {
        "error_text": error_text,
        "category": matched["category"],
        "icon": matched["icon"],
        "root_cause": matched["root_cause"],
        "fix": matched["fix"],
        "traceback": tb
    }


def print_failure_report(report):
    """
    Pretty-print a failure analysis report to the console.
    """
    icon = report["icon"]
    category = report["category"]

    print(f"\n{icon} FAILURE ANALYSIS — {category}")
    print("=" * 40)
    print(f"Error     : {report['error_text']}")
    print(f"Root Cause: {report['root_cause']}")
    print(f"Fix       : {report['fix']}")

    if report.get("traceback"):
        print(f"\nTraceback:\n{report['traceback'].strip()}")

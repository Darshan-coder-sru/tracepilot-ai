"""
Failure Simulation Module
=========================
Inject controlled failures into the research agent for testing
observability, health scoring, and failure analysis.

Usage:
    from dashboard.failure_simulation import simulate_failure, FailureMode

    # Raise a simulated exception
    simulate_failure(FailureMode.TIMEOUT)

    # Or wrap a function call to randomly inject failures
    result = with_random_failure(my_function, failure_rate=0.3)
"""

import time
import random
from enum import Enum


class FailureMode(str, Enum):
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    API_KEY = "api_key"
    NETWORK = "network"
    TOKEN_LIMIT = "token_limit"
    SEARCH = "search"
    RANDOM = "random"


# Maps each FailureMode to a realistic exception message
FAILURE_MESSAGES = {
    FailureMode.TIMEOUT: (
        TimeoutError,
        "Request timed out after 30 seconds. Connection to external service lost."
    ),
    FailureMode.RATE_LIMIT: (
        Exception,
        "429 Too Many Requests: Rate limit exceeded. Please retry after 60 seconds."
    ),
    FailureMode.API_KEY: (
        PermissionError,
        "401 Unauthorized: Invalid API key. Check your GROQ_API_KEY environment variable."
    ),
    FailureMode.NETWORK: (
        ConnectionError,
        "Network connection refused. Unable to reach api.groq.com. Check your internet connection."
    ),
    FailureMode.TOKEN_LIMIT: (
        ValueError,
        "Token limit exceeded: input exceeds max context length of 8192 tokens."
    ),
    FailureMode.SEARCH: (
        RuntimeError,
        "DuckDuckGo search returned no results. The query may be blocked or the service is down."
    ),
}


def simulate_failure(mode: FailureMode = FailureMode.RANDOM):
    """
    Raise a simulated failure exception for the given mode.

    FailureMode.RANDOM picks a mode at random from the full list.
    """

    if mode == FailureMode.RANDOM:
        modes = [m for m in FailureMode if m != FailureMode.RANDOM]
        mode = random.choice(modes)

    exc_class, message = FAILURE_MESSAGES[mode]
    print(f"\n🧪 FAILURE SIMULATION — injecting {mode.value} failure...")
    raise exc_class(message)


def with_random_failure(fn, *args, failure_rate=0.2, mode=FailureMode.RANDOM, **kwargs):
    """
    Call fn(*args, **kwargs) but inject a simulated failure
    with probability `failure_rate` (0.0–1.0).

    Returns the function result on success.
    Raises a simulated exception on injected failure.
    """
    if random.random() < failure_rate:
        simulate_failure(mode)
    return fn(*args, **kwargs)


def run_simulation_demo():
    """
    Run a quick demo of all failure modes without raising — just prints each one.
    """
    print("\n🧪 FAILURE SIMULATION DEMO")
    print("=" * 40)

    modes = [m for m in FailureMode if m != FailureMode.RANDOM]

    for mode in modes:
        exc_class, message = FAILURE_MESSAGES[mode]
        print(f"\n  Mode    : {mode.value}")
        print(f"  Type    : {exc_class.__name__}")
        print(f"  Message : {message}")

    print("\n✅ Demo complete — no exceptions were raised.")


if __name__ == "__main__":
    run_simulation_demo()

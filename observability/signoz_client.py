import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

# Base URL of your SigNoz instance, e.g. https://your-instance.signoz.cloud
# (NOT the OTLP ingestion endpoint — this is the dashboard/API URL)
SIGNOZ_API_URL = os.getenv("SIGNOZ_API_URL")

# Service Account API key from Settings -> Service Accounts -> Keys.
# This is DIFFERENT from SIGNOZ_INGESTION_KEY used to send traces in.
SIGNOZ_API_KEY = os.getenv("SIGNOZ_API_KEY")

SERVICE_NAME = "tracepilot-ai"


def fetch_recent_traces(limit=10, lookback_hours=24, debug_raw=False):
    """
    Fetch the most recent 'research_agent' root spans (one per trace)
    for the tracepilot-ai service, using the SigNoz Trace API.

    Returns a list of dicts:
        {
            "trace_id": str,
            "timestamp": str,
            "duration_ms": float,
            "health_score": int | None,
            "bottleneck": str | None,
            "has_error": bool,
        }

    Raises RuntimeError if SIGNOZ_API_URL / SIGNOZ_API_KEY are missing,
    or requests.HTTPError if the SigNoz API call itself fails.
    """

    if not SIGNOZ_API_URL or not SIGNOZ_API_KEY:
        raise RuntimeError(
            "SIGNOZ_API_URL and SIGNOZ_API_KEY must be set in .env. "
            "Note: SIGNOZ_API_KEY is a Service Account key from "
            "Settings -> Service Accounts in SigNoz — it is different "
            "from the SIGNOZ_INGESTION_KEY used to send traces in."
        )

    end_ms = int(time.time() * 1000)
    start_ms = end_ms - (lookback_hours * 60 * 60 * 1000)

    payload = {
        "start": start_ms,
        "end": end_ms,
        "requestType": "raw",
        "variables": {},
        "compositeQuery": {
            "queries": [
                {
                    "type": "builder_query",
                    "spec": {
                        "name": "A",
                        "signal": "traces",
                        "filter": {
                            "expression": (
                                f"service.name = '{SERVICE_NAME}' "
                                "AND name = 'research_agent'"
                            )
                        },
                        "selectFields": [
                            {"name": "service.name", "fieldContext": "resource"},
                            {"name": "name", "fieldContext": "span"},
                            {"name": "duration_nano", "fieldContext": "span"},
                            {"name": "has_error", "fieldContext": "span"},
                            {"name": "agent.health_score"},
                            {"name": "agent.bottleneck"},
                        ],
                        "order": [
                            {"key": {"name": "timestamp"}, "direction": "desc"}
                        ],
                        "limit": limit,
                        "offset": 0,
                        "disabled": False,
                    },
                }
            ]
        },
    }

    response = requests.post(
        f"{SIGNOZ_API_URL.rstrip('/')}/api/v5/query_range",
        json=payload,
        headers={"SIGNOZ-API-KEY": SIGNOZ_API_KEY},
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if debug_raw:
        # Caller wants to inspect the actual response shape directly.
        return data

    # Actual observed shape from this SigNoz instance:
    # data["data"]["data"]["results"][0]["rows"], each row like:
    # { "timestamp": "...", "data": { "trace_id": ..., "name": ..., ... } }
    try:
        rows = data["data"]["data"]["results"][0].get("rows", [])
    except (KeyError, IndexError, TypeError):
        rows = []

    traces = []

    for row in rows:
        raw = row.get("data", {})

        duration_nano = raw.get("duration_nano") or 0
        health_score = raw.get("agent.health_score")
        bottleneck = raw.get("agent.bottleneck")

        traces.append({
            "trace_id": raw.get("trace_id", "N/A"),
            "timestamp": row.get("timestamp", "N/A"),
            "duration_ms": round(duration_nano / 1_000_000, 2),
            "health_score": health_score,
            "bottleneck": bottleneck,
            "has_error": bool(raw.get("has_error", False)),
        })

    return traces
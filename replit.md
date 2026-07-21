# AgentWatch AI

An AI research agent with a built-in observability dashboard. Ask it a question, it searches the web with DuckDuckGo, calls Groq (llama-3.1-8b-instant), and prints a full performance dashboard alongside the answer.

## Stack

- **Python 3** — entry point: `agent/research_agent.py`
- **Groq** — LLM provider (llama-3.1-8b-instant)
- **DuckDuckGo Search** — web search via `duckduckgo_search`
- **OpenTelemetry + SigNoz** — distributed tracing

## How to run

```bash
python agent/research_agent.py
```

You will be prompted to type a research question. The agent will:
1. Search the web
2. Call Groq AI
3. Print the answer plus a full observability dashboard

## Dashboard features

| Feature | Module |
|---|---|
| 🩺 Agent Health Score | `dashboard/health_score.py` |
| 🚨 Bottleneck Detection | `dashboard/health_score.py` |
| ❌ Intelligent Failure Analysis | `dashboard/failure_analysis.py` |
| 💰 Token & Cost Tracking | `dashboard/token_cost.py` |
| 💡 AI Recommendations | `dashboard/recommendations.py` |
| 📊 Execution Timeline | `dashboard/timeline.py` |
| 🧪 Failure Simulation | `dashboard/failure_simulation.py` |

## Required environment variables / secrets

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY` | Groq API authentication |
| `SIGNOZ_ENDPOINT` | SigNoz OTLP endpoint URL |
| `SIGNOZ_INGESTION_KEY` | SigNoz ingestion key |

## Quick tests

```bash
# Test dashboard modules only (no API keys needed)
python dashboard/test_health.py

# Preview all failure simulation modes (no exceptions raised)
python dashboard/failure_simulation.py
```

## User preferences

- Keep existing project structure and Python stack.

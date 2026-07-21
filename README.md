# 🚀 TracePilot AI

> **AI Agent Observability Platform powered by OpenTelemetry + SigNoz**

TracePilot AI is an intelligent observability platform that monitors AI agents in real time. It traces every stage of an agent's execution, measures performance, detects bottlenecks, analyzes failures, estimates token usage and cost, and provides actionable recommendations through an interactive dashboard.

Built for the **WeMakeDevs × SigNoz Hackathon 2026**.

---

## 🌟 Problem Statement

As AI agents become more complex, developers struggle to answer questions like:

- Why is my AI agent slow?
- Which component is causing latency?
- Why did the agent fail?
- How much does each execution cost?
- How healthy is my AI workflow?

Traditional logging is not enough.

TracePilot AI solves this by providing complete observability for AI agents using OpenTelemetry and SigNoz.

---

# ✨ Features

## 🤖 AI Research Agent

- Uses Groq LLM
- Performs real-time web research
- Generates accurate responses

---

## 📊 Real-Time Observability

- OpenTelemetry instrumentation
- Distributed tracing
- Live trace visualization in SigNoz

---

## 🩺 AI Health Score

Every execution receives a health score based on:

- Total latency
- Search latency
- LLM latency
- Errors
- Token usage

Example:

```
Health Score : 92/100
Status       : Excellent
```

---

## ⚠️ Bottleneck Detection

Automatically identifies the slowest component.

Example:

```
Component : Web Search

Latency : 2.81 sec

Severity : Medium
```

---

## 🚨 Failure Analysis

When an execution fails, TracePilot AI:

- Detects the failure
- Identifies the root cause
- Explains the impact
- Suggests recovery steps

---

## 💰 Token Cost Analysis

Tracks

- Prompt Tokens
- Completion Tokens
- Total Tokens
- Estimated API Cost

---

## 🧠 AI Recommendations

Generates optimization suggestions automatically.

Example:

- Reduce search latency
- Optimize prompts
- Cache search results
- Switch to faster model

---

## 📅 Execution Timeline

Visualizes every stage of the AI pipeline.

```
Planning
     ↓
Web Search
     ↓
LLM Analysis
     ↓
Health Evaluation
     ↓
Recommendations
```

---

## 📈 Historical Analytics

Stores previous runs locally and displays:

- Health trends
- Performance trends
- Error history

---

# 🏗️ Architecture

```
               User
                 │
                 ▼
        Streamlit Dashboard
                 │
                 ▼
        Research AI Agent
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
 Web Search             Groq LLM
      │                     │
      └──────────┬──────────┘
                 ▼
     Health Score Engine
                 │
     ┌───────────┼────────────┐
     ▼           ▼            ▼
 Token Cost  Failure Analysis  Recommendations
                 │
                 ▼
         OpenTelemetry
                 │
                 ▼
              SigNoz
```

---

# 🛠️ Tech Stack

- Python
- Streamlit
- Groq API
- DuckDuckGo Search
- OpenTelemetry
- SigNoz
- SQLite
- Pandas

---

# 📂 Project Structure

```
TracePilot-AI/

│
├── agent/
│   ├── research_agent.py
│
├── dashboard/
│   ├── app.py
│   ├── health_score.py
│   ├── token_cost.py
│   ├── recommendations.py
│   ├── failure_analysis.py
│   ├── timeline.py
│   └── db.py
│
├── observability/
│   ├── telemetry.py
│   └── signoz_client.py
│
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Darshan-coder-sru/tracepilot-ai.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key

SIGNOZ_ENDPOINT=your_endpoint

SIGNOZ_HEADERS=your_headers
```

Run the dashboard

```bash
streamlit run dashboard/app.py
```

---

# 📊 Dashboard

The dashboard provides:

- AI Answer
- Health Score
- Performance Breakdown
- Token Usage
- Cost Analysis
- Failure Report
- Recommendations
- Execution Timeline
- Trace History

---

# 🎯 Future Improvements

- Multi-Agent Monitoring
- Live Streaming Traces
- Grafana Integration
- Slack Alerts
- Email Notifications
- Agent Comparison Dashboard

---

# 👨‍💻 Built For

**WeMakeDevs × SigNoz Hackathon 2026**

---

# ❤️ Acknowledgements

- WeMakeDevs
- SigNoz
- OpenTelemetry
- Groq
- Streamlit

---

# 📜 License

MIT License

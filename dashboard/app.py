import os
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Tracepilot AI",
    page_icon="🛩️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
  /* Global */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  .stApp {
    background: #0a0d14;
    color: #e2e8f0;
  }

  /* Hide default streamlit header */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Hero header ── */
  .tp-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 32px 0 8px 0;
    border-bottom: 1px solid #1e2d45;
    margin-bottom: 28px;
  }
  .tp-logo {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px;
    box-shadow: 0 0 24px rgba(14,165,233,0.35);
  }
  .tp-title {
    font-size: 26px;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0; line-height: 1;
  }
  .tp-subtitle {
    font-size: 13px;
    color: #64748b;
    margin-top: 4px;
    letter-spacing: 0.02em;
  }

  /* ── Input area ── */
  .stTextInput > div > div > input {
    background: #0f1623 !important;
    border: 1.5px solid #1e2d45 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s;
  }
  .stTextInput > div > div > input:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.15) !important;
  }
  .stTextInput > label {
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
  }

  /* ── Primary button ── */
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 28px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.2s, transform 0.1s !important;
    box-shadow: 0 4px 16px rgba(14,165,233,0.3) !important;
  }
  .stButton > button[kind="primary"]:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button[kind="primary"]:disabled {
    opacity: 0.35 !important;
    transform: none !important;
  }

  /* ── Metric cards ── */
  [data-testid="metric-container"] {
    background: #0f1623;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 16px 20px;
  }
  [data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
  }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #0f1623 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid #1e2d45 !important;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 9px !important;
    color: #64748b !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    border: none !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0c1f35, #1a1040) !important;
    color: #38bdf8 !important;
    border: 1px solid #1e3a5f !important;
  }
  .stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px !important;
  }

  /* ── Cards / containers ── */
  .tp-card {
    background: #0f1623;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
  }
  .tp-card-title {
    font-size: 13px;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
  }

  /* ── Score bar ── */
  .tp-score-bar-bg {
    background: #1e2d45;
    border-radius: 100px;
    height: 10px;
    overflow: hidden;
    margin: 12px 0;
  }
  .tp-score-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.5s ease;
  }

  /* ── Severity badges ── */
  .tp-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .tp-badge-high   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
  .tp-badge-medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
  .tp-badge-low    { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
  .tp-badge-ok     { background: rgba(14,165,233,0.15); color: #38bdf8; border: 1px solid rgba(14,165,233,0.3); }

  /* ── Timeline bar ── */
  .stProgress > div > div > div {
    background: linear-gradient(90deg, #0ea5e9, #6366f1) !important;
    border-radius: 100px !important;
  }
  .stProgress > div > div {
    background: #1e2d45 !important;
    border-radius: 100px !important;
  }

  /* ── Status boxes ── */
  .stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 10px !important;
    border-left-width: 3px !important;
    font-size: 14px !important;
  }

  /* ── Divider ── */
  hr {
    border-color: #1e2d45 !important;
    margin: 20px 0 !important;
  }

  /* ── Code block ── */
  .stCodeBlock { border-radius: 10px !important; }

  /* ── Expander ── */
  .streamlit-expanderHeader {
    background: #0f1623 !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-size: 13px !important;
  }

  /* ── Priority row ── */
  .tp-rec-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid #1e2d45;
  }
  .tp-rec-row:last-child { border-bottom: none; }
  .tp-rec-num {
    width: 24px; height: 24px;
    border-radius: 50%;
    background: #1e2d45;
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
  }
  .tp-rec-msg { font-size: 14px; color: #cbd5e1; line-height: 1.5; }
  .tp-rec-area { font-size: 11px; color: #64748b; margin-top: 3px; font-family: 'JetBrains Mono', monospace; }

  /* ── Timeline step row ── */
  .tp-tl-row {
    display: grid;
    grid-template-columns: 160px 1fr 70px 30px;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid #1a2236;
  }
  .tp-tl-row:last-child { border-bottom: none; }
  .tp-tl-label { font-size: 13px; color: #94a3b8; font-weight: 500; }
  .tp-tl-dur   { font-size: 12px; color: #64748b; font-family: 'JetBrains Mono', monospace; text-align: right; }

  /* ── Token stat ── */
  .tp-token-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }
  .tp-token-cell {
    background: #0a0d14;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
  }
  .tp-token-val {
    font-size: 20px;
    font-weight: 700;
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
  }
  .tp-token-lbl {
    font-size: 11px;
    color: #64748b;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div class="tp-header">
  <div class="tp-logo">🛩️</div>
  <div>
    <div class="tp-title">Tracepilot AI</div>
    <div class="tp-subtitle">AI Research Agent · Full Observability Dashboard</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Imports ────────────────────────────────────────────────────
from duckduckgo_search import DDGS
from groq import Groq

from dashboard.health_score import calculate_health_score, get_health_grade, find_bottleneck
from dashboard.failure_analysis import analyze_failure
from dashboard.token_cost import calculate_token_cost, extract_token_usage
from dashboard.recommendations import generate_recommendations
from dashboard.timeline import ExecutionTimeline

MODEL = "llama-3.1-8b-instant"

# ── Input ──────────────────────────────────────────────────────
col_q, col_btn = st.columns([6, 1])
with col_q:
    question = st.text_input(
        "RESEARCH QUERY",
        placeholder="e.g. What is quantum computing?",
        label_visibility="visible"
    )
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run = st.button("▶ Run", type="primary", disabled=not question.strip(), use_container_width=True)

if not run:
    st.stop()

# ── API key check ──────────────────────────────────────────────
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ **GROQ_API_KEY** is not set. Add it in Replit Secrets and restart.")
    st.stop()

client = Groq(api_key=groq_api_key)

# ── Agent execution ────────────────────────────────────────────
agent_start  = time.time()
timeline     = ExecutionTimeline()
error_occurred   = False
failure_report   = None
cost_data        = None
answer           = None
search_latency   = 0.0
llm_latency      = 0.0

# Step 1: Planning
planning_start = time.time()
with st.status("🧠  Planning research…", expanded=False):
    st.write("Formulating search query…")
    search_query = question
    time.sleep(0.1)
timeline.record("Planning", planning_start, time.time(), "ok", "🧠")

# Step 2: Web Search
search_start = time.time()
with st.status("🔍  Searching the web…", expanded=False):
    try:
        raw = []
        with DDGS() as ddgs:
            for r in ddgs.text(search_query, max_results=3):
                raw.append(f"Title: {r['title']}\nContent: {r['body']}")
        search_results = "\n\n".join(raw)
        search_latency = time.time() - search_start
        st.write(f"Found {len(raw)} results in {search_latency:.2f}s")
    except Exception as exc:
        error_occurred = True
        failure_report = analyze_failure(exception=exc)
        search_latency = time.time() - search_start
        search_results = ""
timeline.record("Web Search", search_start, time.time(),
                "error" if error_occurred else "ok", "🔍")

# Step 3: LLM
llm_start = time.time()
response  = None
if not error_occurred:
    with st.status("⚡  Asking Groq AI…", expanded=False):
        try:
            prompt = f"""Answer the user's question using the research results below.

User Question: {question}

Research Results:
{search_results}

Give a clear, accurate, and useful answer."""

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful research AI agent."},
                    {"role": "user",   "content": prompt}
                ],
                temperature=0.7,
                max_tokens=700
            )
            answer      = response.choices[0].message.content
            llm_latency = time.time() - llm_start

            pt, ct  = extract_token_usage(response)
            cost_data = calculate_token_cost(model=MODEL, prompt_tokens=pt, completion_tokens=ct)
            st.write(f"Answer generated in {llm_latency:.2f}s")
        except Exception as exc:
            error_occurred = True
            failure_report = analyze_failure(exception=exc)
            llm_latency = time.time() - llm_start

timeline.record("LLM Analysis", llm_start, time.time(),
                "error" if error_occurred else "ok", "⚡")

total_latency = time.time() - agent_start

# ── Compute metrics ────────────────────────────────────────────
total_tokens  = cost_data["total_tokens"] if cost_data else 0
health_score  = calculate_health_score(
    total_latency=total_latency, search_latency=search_latency,
    llm_latency=llm_latency, error=error_occurred, token_count=total_tokens
)
grade, status_label = get_health_grade(health_score)
bottleneck    = find_bottleneck(search_latency, llm_latency)
recommendations = generate_recommendations(
    health_score=health_score, bottleneck=bottleneck,
    total_latency=total_latency, search_latency=search_latency,
    llm_latency=llm_latency, token_cost_data=cost_data,
    error=error_occurred, failure_report=failure_report
)

st.divider()

# ── Top KPI row ────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("🩺 Health Score", f"{health_score}/100", f"Grade {grade} — {status_label}")
k2.metric("⏱️ Total Time",   f"{total_latency:.2f}s")
k3.metric("🔍 Search",       f"{search_latency:.2f}s")
k4.metric("⚡ LLM",          f"{llm_latency:.2f}s")

st.divider()

# ── Tabs ───────────────────────────────────────────────────────
(tab_ans, tab_health, tab_bot, tab_fail, tab_cost, tab_rec, tab_tl) = st.tabs([
    "📄 Answer",
    "🩺 Health Score",
    "🚨 Bottleneck",
    "❌ Failure Analysis",
    "💰 Token & Cost",
    "💡 Recommendations",
    "📊 Timeline",
])

# ── Tab: Answer ────────────────────────────────────────────────
with tab_ans:
    if answer:
        st.markdown(
            f'<div class="tp-card"><div class="tp-card-title">Agent Response</div>'
            f'<div style="font-size:15px;line-height:1.7;color:#cbd5e1">{answer}</div></div>',
            unsafe_allow_html=True
        )
    elif error_occurred:
        st.error("Agent failed to produce an answer. See the **Failure Analysis** tab.")
    else:
        st.info("No answer returned.")

# ── Tab: Health Score ──────────────────────────────────────────
with tab_health:
    if health_score >= 75:
        bar_color = "linear-gradient(90deg,#22c55e,#4ade80)"
        grade_color = "#4ade80"
    elif health_score >= 40:
        bar_color = "linear-gradient(90deg,#f59e0b,#fbbf24)"
        grade_color = "#fbbf24"
    else:
        bar_color = "linear-gradient(90deg,#ef4444,#f87171)"
        grade_color = "#f87171"

    st.markdown(f"""
    <div class="tp-card">
      <div class="tp-card-title">Agent Health Score</div>
      <div style="display:flex;align-items:baseline;gap:12px">
        <span style="font-size:48px;font-weight:800;font-family:'JetBrains Mono',monospace;color:{grade_color}">{health_score}</span>
        <span style="font-size:20px;color:#64748b;font-weight:600">/100</span>
        <span style="font-size:22px;font-weight:700;color:{grade_color};margin-left:8px">Grade {grade}</span>
      </div>
      <div class="tp-score-bar-bg">
        <div class="tp-score-bar-fill" style="width:{health_score}%;background:{bar_color}"></div>
      </div>
      <div style="font-size:13px;color:#64748b">{status_label}</div>
    </div>

    <div class="tp-card">
      <div class="tp-card-title">Scoring Breakdown</div>
      <table style="width:100%;font-size:13px;border-collapse:collapse;color:#94a3b8">
        <tr style="border-bottom:1px solid #1e2d45">
          <th style="text-align:left;padding:8px 0;color:#64748b;font-weight:500">Condition</th>
          <th style="text-align:right;padding:8px 0;color:#64748b;font-weight:500">Penalty</th>
        </tr>
        <tr style="border-bottom:1px solid #1a2236"><td style="padding:8px 0">Error occurred</td><td style="text-align:right;color:#f87171">−40 pts</td></tr>
        <tr style="border-bottom:1px solid #1a2236"><td style="padding:8px 0">Total latency &gt; 15s</td><td style="text-align:right;color:#f87171">−30 pts</td></tr>
        <tr style="border-bottom:1px solid #1a2236"><td style="padding:8px 0">Total latency &gt; 10s</td><td style="text-align:right;color:#fbbf24">−20 pts</td></tr>
        <tr style="border-bottom:1px solid #1a2236"><td style="padding:8px 0">Total latency &gt; 5s</td><td style="text-align:right;color:#fbbf24">−10 pts</td></tr>
        <tr style="border-bottom:1px solid #1a2236"><td style="padding:8px 0">Search 2× slower than LLM</td><td style="text-align:right;color:#fbbf24">−10 pts</td></tr>
        <tr><td style="padding:8px 0">Token usage &gt; 2,000</td><td style="text-align:right;color:#fbbf24">−5 pts</td></tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

# ── Tab: Bottleneck ────────────────────────────────────────────
with tab_bot:
    sev = bottleneck["severity"]
    sev_class = {"HIGH":"tp-badge-high","MEDIUM":"tp-badge-medium","LOW":"tp-badge-low"}.get(sev,"tp-badge-ok")
    st.markdown(f"""
    <div class="tp-card">
      <div class="tp-card-title">Bottleneck Detection</div>
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
        <span style="font-size:22px;font-weight:700;color:#e2e8f0">{bottleneck['component']}</span>
        <span class="tp-badge {sev_class}">{sev}</span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <div class="tp-token-cell">
          <div class="tp-token-val">{bottleneck['latency']:.2f}s</div>
          <div class="tp-token-lbl">Component Latency</div>
        </div>
        <div class="tp-token-cell">
          <div class="tp-token-val" style="color:#818cf8">{total_latency:.2f}s</div>
          <div class="tp-token-lbl">Total Latency</div>
        </div>
      </div>
      <div style="margin-top:16px;padding:12px;background:#0a0d14;border-radius:10px;border:1px solid #1e2d45">
        <div style="font-size:12px;color:#64748b;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.05em">Message</div>
        <div style="font-size:14px;color:#cbd5e1">{bottleneck['message']}</div>
      </div>
      <div style="margin-top:10px;padding:12px;background:#0c1a2e;border-radius:10px;border:1px solid #1e3a5f">
        <div style="font-size:12px;color:#38bdf8;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.05em">💡 Suggestion</div>
        <div style="font-size:14px;color:#93c5fd">{bottleneck['suggestion']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Tab: Failure Analysis ──────────────────────────────────────
with tab_fail:
    if error_occurred and failure_report:
        st.markdown(f"""
        <div class="tp-card" style="border-color:rgba(239,68,68,0.3)">
          <div class="tp-card-title" style="color:#f87171">Intelligent Failure Analysis</div>
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
            <span style="font-size:28px">{failure_report['icon']}</span>
            <div>
              <div style="font-size:16px;font-weight:700;color:#f87171">{failure_report['category']}</div>
              <div style="font-size:12px;color:#64748b;font-family:'JetBrains Mono',monospace;margin-top:2px">{failure_report['error_text'][:80]}…</div>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
            <div style="padding:12px;background:#0a0d14;border-radius:10px;border:1px solid #2d1515">
              <div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px">Root Cause</div>
              <div style="font-size:13px;color:#fca5a5">{failure_report['root_cause']}</div>
            </div>
            <div style="padding:12px;background:#0a0d14;border-radius:10px;border:1px solid #1e3a2d">
              <div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px">Suggested Fix</div>
              <div style="font-size:13px;color:#86efac">{failure_report['fix']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if failure_report.get("traceback"):
            with st.expander("Full traceback"):
                st.code(failure_report["traceback"], language="python")
    else:
        st.markdown("""
        <div class="tp-card" style="border-color:rgba(34,197,94,0.3);text-align:center;padding:36px">
          <div style="font-size:36px">✅</div>
          <div style="font-size:16px;font-weight:600;color:#4ade80;margin-top:8px">No failures detected</div>
          <div style="font-size:13px;color:#64748b;margin-top:4px">This run completed without errors.</div>
        </div>
        """, unsafe_allow_html=True)

# ── Tab: Token & Cost ──────────────────────────────────────────
with tab_cost:
    if cost_data:
        st.markdown(f"""
        <div class="tp-card">
          <div class="tp-card-title">Token Usage</div>
          <div class="tp-token-grid">
            <div class="tp-token-cell">
              <div class="tp-token-val">{cost_data['prompt_tokens']:,}</div>
              <div class="tp-token-lbl">Prompt Tokens</div>
            </div>
            <div class="tp-token-cell">
              <div class="tp-token-val" style="color:#818cf8">{cost_data['completion_tokens']:,}</div>
              <div class="tp-token-lbl">Completion Tokens</div>
            </div>
            <div class="tp-token-cell">
              <div class="tp-token-val" style="color:#4ade80">{cost_data['total_tokens']:,}</div>
              <div class="tp-token-lbl">Total Tokens</div>
            </div>
          </div>
        </div>
        <div class="tp-card">
          <div class="tp-card-title">Cost Breakdown</div>
          <div class="tp-token-grid">
            <div class="tp-token-cell">
              <div class="tp-token-val" style="font-size:16px">${cost_data['input_cost_usd']:.6f}</div>
              <div class="tp-token-lbl">Input Cost</div>
            </div>
            <div class="tp-token-cell">
              <div class="tp-token-val" style="font-size:16px;color:#818cf8">${cost_data['output_cost_usd']:.6f}</div>
              <div class="tp-token-lbl">Output Cost</div>
            </div>
            <div class="tp-token-cell">
              <div class="tp-token-val" style="font-size:16px;color:#4ade80">${cost_data['total_cost_usd']:.6f}</div>
              <div class="tp-token-lbl">Total Cost</div>
            </div>
          </div>
          <div style="font-size:12px;color:#475569;font-family:'JetBrains Mono',monospace">Model: {cost_data['model']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No token data — LLM did not complete successfully.")

# ── Tab: Recommendations ───────────────────────────────────────
with tab_rec:
    badge = {"HIGH":"tp-badge-high","MEDIUM":"tp-badge-medium","LOW":"tp-badge-low"}
    rows_html = ""
    for i, rec in enumerate(recommendations, 1):
        bc = badge.get(rec["priority"], "tp-badge-ok")
        rows_html += f"""
        <div class="tp-rec-row">
          <div class="tp-rec-num">{i}</div>
          <div style="flex:1">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
              <span style="font-size:16px">{rec['icon']}</span>
              <span class="tp-badge {bc}">{rec['priority']}</span>
              <span style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace">{rec['area']}</span>
            </div>
            <div class="tp-rec-msg">{rec['message']}</div>
          </div>
        </div>"""
    st.markdown(f'<div class="tp-card"><div class="tp-card-title">AI Recommendations</div>{rows_html}</div>',
                unsafe_allow_html=True)

# ── Tab: Timeline ──────────────────────────────────────────────
with tab_tl:
    if timeline.steps:
        total_dur = max(s["end"] for s in timeline.steps)
        rows_html = ""
        for step in timeline.steps:
            pct  = min((step["end"] - step["start"]) / max(total_dur, 0.001), 1.0)
            ok   = "✅" if step["status"] == "ok" else "❌"
            rows_html += f"""
            <div class="tp-tl-row">
              <div class="tp-tl-label">{step['icon']} {step['name']}</div>
              <div>__PROGRESS_{step['name']}__</div>
              <div class="tp-tl-dur">{step['duration']:.2f}s</div>
              <div style="font-size:14px">{ok}</div>
            </div>"""

        st.markdown(f'<div class="tp-card"><div class="tp-card-title">Execution Timeline</div>',
                    unsafe_allow_html=True)
        for step in timeline.steps:
            pct  = min((step["end"] - step["start"]) / max(total_dur, 0.001), 1.0)
            ok   = "✅" if step["status"] == "ok" else "❌"
            c1, c2, c3, c4 = st.columns([2, 5, 1, 1])
            c1.markdown(f"<div style='font-size:13px;color:#94a3b8;padding-top:6px'>{step['icon']} {step['name']}</div>", unsafe_allow_html=True)
            c2.progress(pct)
            c3.markdown(f"<div style='font-size:12px;color:#64748b;font-family:monospace;text-align:right;padding-top:6px'>{step['duration']:.2f}s</div>", unsafe_allow_html=True)
            c4.markdown(f"<div style='padding-top:4px'>{ok}</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='margin-top:8px;font-size:12px;color:#475569;font-family:monospace'>Total: {total_latency:.2f}s wall-clock time</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No timeline data recorded.")

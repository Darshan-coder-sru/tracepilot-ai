import os
import sqlite3
from datetime import datetime, timezone

# Store the database at the project root, alongside requirements.txt
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tracepilot.db"
)


def init_db():
    """
    Create the runs table if it doesn't already exist, and add any
    new columns to older databases that were created before this
    schema was extended (safe to call every time).
    """

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT,
                total_latency REAL,
                search_latency REAL,
                llm_latency REAL,
                health_score INTEGER,
                health_grade TEXT,
                bottleneck_component TEXT,
                bottleneck_message TEXT,
                total_tokens INTEGER,
                total_cost_usd REAL,
                error INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        # Migrate older databases that predate the extra columns.
        existing_cols = {
            row[1] for row in conn.execute("PRAGMA table_info(runs)")
        }

        new_columns = {
            "health_grade": "TEXT",
            "total_tokens": "INTEGER",
            "total_cost_usd": "REAL",
        }

        for col_name, col_type in new_columns.items():
            if col_name not in existing_cols:
                conn.execute(
                    f"ALTER TABLE runs ADD COLUMN {col_name} {col_type}"
                )

        conn.commit()


def log_run(question, result):
    """
    Save one agent run to the local history log.

    `result` is the dict returned by research_agent():
        answer, total_latency, search_latency, llm_latency,
        health_score, health_grade, bottleneck, cost_data, error, ...

    Logging failures are swallowed (never raised) so a DB hiccup
    can never crash an actual agent run.
    """

    init_db()

    bottleneck = result.get("bottleneck") or {}
    cost_data = result.get("cost_data") or {}

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                INSERT INTO runs (
                    timestamp, question, answer,
                    total_latency, search_latency, llm_latency,
                    health_score, health_grade,
                    bottleneck_component, bottleneck_message,
                    total_tokens, total_cost_usd,
                    error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    question,
                    result.get("answer"),
                    result.get("total_latency"),
                    result.get("search_latency"),
                    result.get("llm_latency"),
                    result.get("health_score"),
                    result.get("health_grade"),
                    bottleneck.get("component"),
                    bottleneck.get("message"),
                    cost_data.get("total_tokens"),
                    cost_data.get("total_cost_usd"),
                    int(bool(result.get("error"))),
                )
            )
            conn.commit()
    except Exception as e:
        # Don't let a logging failure take down the agent.
        print(f"⚠️ Could not log run to history: {e}")


def get_run_history(limit=20):
    """
    Return the most recent runs, newest first, as a list of dicts.
    """

    init_db()

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.execute(
            "SELECT * FROM runs ORDER BY id DESC LIMIT ?",
            (limit,)
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]
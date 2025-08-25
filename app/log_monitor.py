^C[ec2-user@ip-172-31-22-75 app]$ cat log_monitor.py
import os
import random
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, Response, Query
from prometheus_client import (
    Counter,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = FastAPI(title="Log Monitor")

# ---- Config ----
# Default log levels; can be extended by setting env LOG_LEVELS="INFO,WARNING,ERROR,DEBUG"
DEFAULT_LEVELS = ["INFO", "WARNING", "ERROR"]
LEVELS: List[str] = [
    lvl.strip().upper()
    for lvl in os.getenv("LOG_LEVELS", ",".join(DEFAULT_LEVELS)).split(",")
    if lvl.strip()
]

# ---- In-memory log store (demo only) ----
logs: List[Dict] = []

# ---- Prometheus metrics (dynamic per-level counters + totals) ----
TOTAL_LOGS = Counter("total_logs", "Total logs processed")
# Keep a registry of per-level counters so adding a new level is trivial
LEVEL_COUNTERS: Dict[str, Counter] = {}


def get_level_counter(level: str) -> Counter:
    """
    Return a Counter for the given level. Create it on first use so
    adding a new level only requires adding it to LEVELS or passing it at runtime.
    Metric name pattern: <lowercase>_logs (e.g., info_logs, warning_logs)
    """
    key = level.upper()
    if key not in LEVEL_COUNTERS:
        metric_name = f"{key.lower()}_logs"
        LEVEL_COUNTERS[key] = Counter(
            metric_name,
            f"{key.title()} logs processed",
        )
    return LEVEL_COUNTERS[key]


def record_log(level: str, message: str = "This is a sample log message") -> Dict:
    level = level.upper()
    if level not in LEVELS:
        # If a new level is used ad-hoc, accept it and expose a counter for it.
        LEVELS.append(level)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
    }
    logs.append(entry)

    # Update metrics
    TOTAL_LOGS.inc()
    get_level_counter(level).inc()
    return entry


@app.get("/", tags=["health"])
def root():
    return {"message": "Log Monitor API running", "levels": LEVELS}


@app.get("/generate-log", tags=["logs"])
def generate_log(level: Optional[str] = Query(default=None, description="Override level, e.g. DEBUG")):
    """
    Generate one log. If ?level= is provided, use it; otherwise pick randomly from LEVELS.
    """
    lvl = level.upper() if level else random.choice(LEVELS)
    entry = record_log(lvl)
    return {"status": "log generated", "level": entry["level"], "total_logs": len(logs)}


@app.get("/metrics-json", tags=["metrics"])
def metrics_json():
    """
    Convenience JSON view of counters for quick eyeballing (not used by Prometheus).
    """
    data = { "total_logs": int(TOTAL_LOGS._value.get()) }  # type: ignore[attr-defined]
    for lvl, counter in LEVEL_COUNTERS.items():
        data[f"{lvl.lower()}_logs"] = int(counter._value.get())  # type: ignore[attr-defined]
    return data


@app.get("/metrics")
def metrics_prometheus():
    """
    Prometheus scrape endpoint. Exposes standard text exposition format.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
[ec2-user@ip-172-31-22-75 app]$

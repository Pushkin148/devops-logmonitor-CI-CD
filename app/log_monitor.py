import os
import random
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, Response, Query
from prometheus_client import (
    Counter,
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY  # <-- added for dynamic registration
)

app = FastAPI(title="Log Monitor")

# ---- Config ----
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
LEVEL_COUNTERS: Dict[str, Counter] = {}


def get_level_counter(level: str) -> Counter:
    key = level.upper()
    if key not in LEVEL_COUNTERS:
        metric_name = f"{key.lower()}_logs"
        c = Counter(metric_name, f"{key.title()} logs processed")
        REGISTRY.register(c)  # <-- ensures new levels are visible to Prometheus
        LEVEL_COUNTERS[key] = c
    return LEVEL_COUNTERS[key]


def record_log(level: str, message: str = "This is a sample log message") -> Dict:
    level = level.upper()
    if level not in LEVELS:
        LEVELS.append(level)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
    }
    logs.append(entry)

    TOTAL_LOGS.inc()
    get_level_counter(level).inc()
    return entry


@app.get("/", tags=["health"])
def root():
    return {"message": "Log Monitor API running", "levels": LEVELS}


@app.get("/generate-log", tags=["logs"])
def generate_log(level: Optional[str] = Query(default=None, description="Override level, e.g. DEBUG")):
    lvl = level.upper() if level else random.choice(LEVELS)
    entry = record_log(lvl)
    return {"status": "log generated", "level": entry["level"], "total_logs": len(logs)}


@app.get("/metrics-json", tags=["metrics"])
def metrics_json():
    data = {"total_logs": int(TOTAL_LOGS._value.get())}  # type: ignore[attr-defined]
    for lvl, counter in LEVEL_COUNTERS.items():
        data[f"{lvl.lower()}_logs"] = int(counter._value.get())  # type: ignore[attr-defined]
    return data


@app.get("/metrics")
def metrics_prometheus():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

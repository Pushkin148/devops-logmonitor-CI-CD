from fastapi import FastAPI, Response
from datetime import datetime
import random

app = FastAPI()

# Fake log store
logs = []

# Simulate log generation
def generate_fake_log():
    levels = ["INFO", "WARNING", "ERROR"]
    log = {
        "timestamp": datetime.now().isoformat(),
        "level": random.choice(levels),
        "message": "This is a sample log message"
    }
    logs.append(log)

@app.get("/generate-log")
def generate_log():
    generate_fake_log()
    return {"status": "log generated", "total_logs": len(logs)}

# JSON metrics (existing one - kept as is, plus new warning_logs)
@app.get("/metrics-json")
def metrics_json():
    error_count = sum(1 for log in logs if log["level"] == "ERROR")
    warning_count = sum(1 for log in logs if log["level"] == "WARNING")
    return {
        "total_logs": len(logs),
        "error_logs": error_count,
        "warning_logs": warning_count
    }

# Prometheus-compatible metrics (existing plus warning_logs)
@app.get("/metrics")
def metrics_prometheus():
    error_count = sum(1 for log in logs if log["level"] == "ERROR")
    warning_count = sum(1 for log in logs if log["level"] == "WARNING")
    metrics_data = (
        f"total_logs {len(logs)}\n"
        f"error_logs {error_count}\n"
        f"warning_logs {warning_count}\n"
    )
    return Response(content=metrics_data, media_type="text/plain")

@app.get("/")
def root():
    return {"message": "Log Monitor API running"}

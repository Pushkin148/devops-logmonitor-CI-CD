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

# JSON metrics
@app.get("/metrics-json")
def metrics_json():
    metric_counts = {}
    for log in logs:
        metric_counts[log["level"].lower() + "_logs"] = metric_counts.get(log["level"].lower() + "_logs", 0) + 1
    metric_counts["total_logs"] = len(logs)
    return metric_counts

# Prometheus metrics
@app.get("/metrics")
def metrics_prometheus():
    metric_counts = {}
    for log in logs:
        metric_name = log["level"].lower() + "_logs"
        metric_counts[metric_name] = metric_counts.get(metric_name, 0) + 1
    metric_counts["total_logs"] = len(logs)
    metrics_data = "\n".join(f"{k} {v}" for k, v in metric_counts.items())
    return Response(content=metrics_data, media_type="text/plain")

@app.get("/")
def root():
    return {"message": "Log Monitor API running"}

# .api/app.py

from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest
import os, random, time

app = Flask(__name__)
error_counter = Counter("app_errors_total", "Total API errors")
request_latency = Histogram(
    "app_request_latency_seconds", 
    "Request latency",
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2, 5]
)

@app.route("/")
@request_latency.time()
def home():
    fail_mode = os.path.exists("/tmp/fail_mode.flag")
    if fail_mode or random.random() < 0.4:
        error_counter.inc()
        return "API Error!", 500
    return "API OK!"

@app.route("/slow")
@request_latency.time()
def slow():
    # Simulate latency spike
    time.sleep(random.uniform(1.0, 3.0))
    return "Slow response simulated"


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
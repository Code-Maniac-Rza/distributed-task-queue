from prometheus_client import Counter, Histogram, start_http_server

TASK_PROCESSED = Counter("tasks_processed_total", "Processed tasks")
TASK_FAILED = Counter("tasks_failed_total", "Failed tasks")
TASK_LATENCY = Histogram("task_latency_seconds", "Task processing time")

def start_metrics_server():
    start_http_server(8001)

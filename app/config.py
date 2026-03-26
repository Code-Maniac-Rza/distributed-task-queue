import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

QUEUE_NAME = "task_queue"
RESULT_STORE = "task_results"
RETRY_LIMIT = 3

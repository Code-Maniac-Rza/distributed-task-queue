import time
from app.queue import dequeue_task, store_result, requeue_task
from app.tasks import process_task
from app.config import RETRY_LIMIT
from app.metrics import TASK_PROCESSED, TASK_FAILED, TASK_LATENCY, start_metrics_server

def worker():
    print("Worker started...")

    while True:
        task = dequeue_task()
        start_time = time.time()

        try:
            result = process_task(task["type"], task["payload"])
            store_result(task["id"], {
                "status": "completed",
                "result": result
            })
            TASK_PROCESSED.inc()

        except Exception as e:
            task["retries"] += 1

            if task["retries"] < RETRY_LIMIT:
                print(f"Retrying task {task['id']} ({task['retries']})")
                requeue_task(task)
            else:
                store_result(task["id"], {
                    "status": "failed",
                    "error": str(e)
                })
                TASK_FAILED.inc()

        finally:
            TASK_LATENCY.observe(time.time() - start_time)

        time.sleep(0.1)

if __name__ == "__main__":
    start_metrics_server()
    worker()

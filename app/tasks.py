import time
import random

REQUIRED_FIELDS = {
    "square": ["number"],
    "fail_random": [],
}

def process_task(task_type, payload):
    if task_type == "square":
        time.sleep(2)
        return payload["number"] ** 2

    elif task_type == "fail_random":
        time.sleep(1)
        if random.random() < 0.5:
            raise Exception("Random failure occurred")
        return "Success"

    else:
        return "Unknown task"

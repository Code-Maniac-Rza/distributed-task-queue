Distributed Task Queue

A simple distributed task queue built with FastAPI, Redis, and Docker. Tasks get submitted via an API, processed by a worker in the background, and results can be fetched anytime. Prometheus tracks the metrics.


How it works

You POST a task to the API. The API pushes it into a Redis queue. A worker picks it up, processes it, and stores the result back in Redis. If a task fails, the worker retries it up to 3 times before marking it as failed.


Getting started

Make sure you have Docker and Docker Compose installed, then just run:

docker-compose up --build

The API will be available at http://localhost:8000
Prometheus will be at http://localhost:9090


Submitting a task

POST http://localhost:8000/submit

Example body:
{
  "task_type": "square",
  "payload": { "number": 4 }
}

You'll get back a task_id. Use that to check the result.


Checking a result

GET http://localhost:8000/result/{task_id}

The response will either say pending (still being processed), completed with the result, or failed with the error.


Supported task types

square - takes a number and returns its square
fail_random - randomly succeeds or fails, useful for testing retries


Project structure

app/config.py - Redis connection settings and queue config
app/queue.py - enqueue, dequeue, and result storage via Redis
app/tasks.py - actual task logic lives here
app/worker.py - background worker that processes tasks and handles retries
app/main.py - FastAPI routes
app/metrics.py - Prometheus counters and histograms


Adding a new task type

Add the logic in app/tasks.py inside the process_task function, then add the required fields to the REQUIRED_FIELDS dict at the top of the same file. That's it.


Notes

Retries preserve the original task ID so polling always works.
Latency is tracked for both successful and failed tasks.
Redis uses a connection pool so it handles concurrent workers fine.

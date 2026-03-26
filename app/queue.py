import redis
import json
import uuid
from app.config import REDIS_HOST, REDIS_PORT, QUEUE_NAME, RESULT_STORE

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def enqueue_task(task_type, payload):
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "type": task_type,
        "payload": payload,
        "retries": 0
    }
    r.lpush(QUEUE_NAME, json.dumps(task))
    return task_id

def requeue_task(task):
    r.lpush(QUEUE_NAME, json.dumps(task))

def dequeue_task():
    _, task = r.brpop(QUEUE_NAME)
    return json.loads(task)

def store_result(task_id, result):
    r.hset(RESULT_STORE, task_id, json.dumps(result))

def get_result(task_id):
    result = r.hget(RESULT_STORE, task_id)
    return json.loads(result) if result else None

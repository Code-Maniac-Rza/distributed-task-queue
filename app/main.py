from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.queue import enqueue_task, get_result
from app.tasks import REQUIRED_FIELDS

app = FastAPI()

class TaskRequest(BaseModel):
    task_type: str
    payload: dict

@app.get("/")
def home():
    return {"message": "Distributed Task Queue Running"}

@app.post("/submit")
def submit_task(task: TaskRequest):
    required = REQUIRED_FIELDS.get(task.task_type)
    if required is None:
        raise HTTPException(status_code=400, detail="Unknown task type")
    missing = [f for f in required if f not in task.payload]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing fields: {missing}")
    task_id = enqueue_task(task.task_type, task.payload)
    return {"task_id": task_id}

@app.get("/result/{task_id}")
def fetch_result(task_id: str):
    result = get_result(task_id)
    return result or {"status": "pending"}

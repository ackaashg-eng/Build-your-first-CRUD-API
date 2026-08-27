from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

class TaskChange(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

app =FastAPI()

tasks = [
    {"id":1,"title":"Task1" , "done": True},
    {"id":2, "title": "Task2", "done": False},
    {"id":3, "title": "Task3", "done": False}
]

@app.get("/")
def root():
    return{
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def task():
    return tasks

@app.get("/tasks/{id}")
def get_task(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskChange):
    title = task.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskChange):
    for task in tasks:
        if task["id"] == task_id:
            if update.title is not None:
                title = update.title.strip()
                if not title:
                    raise HTTPException(status_code=400, detail="title cannot be empty")
                task["title"] = title
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
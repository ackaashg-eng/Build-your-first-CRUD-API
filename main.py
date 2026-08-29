from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from database import create_table, insert_example_tasks
class TaskCreate(BaseModel):
    title: str

class TaskChange(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

app =FastAPI()


create_table()
insert_example_tasks()

tasks = [
    {"id":1,"title":"Task1" , "done": True},
    {"id":2, "title": "Task2", "done": False},
    {"id":3, "title": "Task3", "done": False}
]

@app.get("/")
def root():
    """Returns basic info about this API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    """Health check — confirms the server is running."""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    """Returns the full list of tasks."""
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Returns a single task by id, or 404 if it doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Creates a new task. Requires a non-empty title. Returns 400 if invalid."""
    title = task.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskChange):
    """Updates a task's title and/or done status. 404 if not found, 400 if title is invalid."""
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

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Deletes a task by id. 404 if it doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

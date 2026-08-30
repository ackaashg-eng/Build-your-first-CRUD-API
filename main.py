from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from database import (
    create_table,
    insert_example_tasks,
    get_all_tasks,
    get_task_by_id
)


class TaskCreate(BaseModel):
    title: str


class TaskChange(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


app = FastAPI()


create_table()
insert_example_tasks()


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
    return get_all_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Returns a single task by id, or 404 if it doesn't exist."""

    task = get_task_by_id(task_id)

    if task is not None:
        return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
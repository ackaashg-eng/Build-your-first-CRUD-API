from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from database import (
    create_table,
    insert_example_tasks,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task
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

@app.post("/tasks", status_code=201)
def create_task_endpoint(task: TaskCreate):
    """Creates a new task. Requires a non-empty title. Returns 400 if invalid."""

    title = task.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="title is required and cannot be empty"
        )

    return create_task(title)

@app.post("/tasks", status_code=201)
def create_task_endpoint(task: TaskCreate):
    """Creates a new task. Requires a non-empty title. Returns 400 if invalid."""

    title = task.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="title is required and cannot be empty"
        )

    return create_task(title)
@app.put("/tasks/{task_id}")
def update_task_endpoint(task_id: int, update: TaskChange):
    """Updates a task's title and/or done status."""

    existing_task = get_task_by_id(task_id)

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    title = existing_task["title"]
    done = existing_task["done"]

    if update.title is not None:
        title = update.title.strip()

        if not title:
            raise HTTPException(
                status_code=400,
                detail="title cannot be empty"
            )

    if update.done is not None:
        done = update.done

    update_task(
        task_id,
        title,
        done
    )

    return {
        "id": task_id,
        "title": title,
        "done": done
    }


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int):
    """Deletes a task by id. 404 if it doesn't exist."""

    existing_task = get_task_by_id(task_id)

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    delete_task(task_id)

    return None

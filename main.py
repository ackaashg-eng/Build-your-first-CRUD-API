from fastapi import FastAPI, HTTPException

from database import (
    create_table,
    insert_example_tasks,
    get_all_tasks,
    get_task_by_id
)


app = FastAPI()


create_table()
insert_example_tasks()


@app.get("/tasks")
def get_tasks():

    rows = get_all_tasks()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        })

    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    row = get_task_by_id(task_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }
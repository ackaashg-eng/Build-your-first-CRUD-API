from fastapi import FastAPI, HTTPException

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


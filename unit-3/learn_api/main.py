from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Data
# -----------------------------

tasks = []

next_id = 1


# -----------------------------
# Model
# -----------------------------

class Task(BaseModel):
    title: str
    description: str = ""
    priority: str = "Medium"
    is_completed: bool = False


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Todo API is running"
    }


# -----------------------------
# GET - All Tasks
# -----------------------------

@app.get("/tasks")
def get_tasks():

    return tasks


# -----------------------------
# GET - Single Task
# -----------------------------

@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:

        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# -----------------------------
# POST - Add Task
# -----------------------------

@app.post("/tasks")
def add_task(task: Task):

    global next_id

    new_task = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "is_completed": task.is_completed
    }

    tasks.append(new_task)

    next_id += 1

    return {
        "message": "Task added successfully",
        "task": new_task
    }


# -----------------------------
# PUT - Update Task
# -----------------------------

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):

    for i in range(len(tasks)):

        if tasks[i]["id"] == task_id:

            tasks[i]["title"] = task.title
            tasks[i]["description"] = task.description
            tasks[i]["priority"] = task.priority
            tasks[i]["is_completed"] = task.is_completed

            return {
                "message": "Task updated successfully",
                "task": tasks[i]
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# -----------------------------
# PUT - Toggle Complete
# -----------------------------

@app.put("/tasks/{task_id}/toggle")
def toggle_task(task_id: int):

    for task in tasks:

        if task["id"] == task_id:

            task["is_completed"] = not task["is_completed"]

            return {
                "message": "Task status changed",
                "task": task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# -----------------------------
# DELETE - Delete Task
# -----------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)

            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# -----------------------------
# DELETE - Clear Completed
# -----------------------------

@app.delete("/clear-completed")
def clear_completed():

    global tasks

    tasks = [
        task for task in tasks
        if task["is_completed"] == False
    ]

    return {
        "message": "Completed tasks deleted"
    }
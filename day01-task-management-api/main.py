from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="Task Management API",
    description="A simple REST API for managing tasks",
    version="1.0.0"
)

# In-memory storage
tasks_db: Dict[str, dict] = {}


# -----------------------------
# Pydantic Models
# -----------------------------

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime


# -----------------------------
# Helper Function
# -----------------------------

def get_task_or_404(task_id: str):
    task = tasks_db.get(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# -----------------------------
# Create Task
# -----------------------------

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):

    task_id = str(uuid.uuid4())
    now = datetime.utcnow()

    new_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": False,
        "created_at": now,
        "updated_at": now
    }

    tasks_db[task_id] = new_task

    return new_task


# -----------------------------
# Get All Tasks
# -----------------------------

@app.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks():
    return list(tasks_db.values())


# -----------------------------
# Get Single Task
# -----------------------------

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):

    task = get_task_or_404(task_id)

    return task


# -----------------------------
# Update Task
# -----------------------------

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate):

    task = get_task_or_404(task_id)

    if task_update.title is not None:
        task["title"] = task_update.title

    if task_update.description is not None:
        task["description"] = task_update.description

    task["updated_at"] = datetime.utcnow()

    return task


# -----------------------------
# Toggle Task Completion
# -----------------------------

@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(task_id: str):

    task = get_task_or_404(task_id)

    task["completed"] = not task["completed"]

    task["updated_at"] = datetime.utcnow()

    return task


# -----------------------------
# Delete Task
# -----------------------------

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):

    task = get_task_or_404(task_id)

    del tasks_db[task_id]

    return None
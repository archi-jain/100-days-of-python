from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

import models
import schemas

from database import engine, get_db

# Create tables (simple alternative to migrations)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API with PostgreSQL",
    version="2.0.0"
)


# -----------------------------
# Create Task
# -----------------------------

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):

    new_task = models.Task(
        title=task.title,
        description=task.description
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task


# -----------------------------
# Get All Tasks
# -----------------------------

@app.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    tasks = db.query(models.Task).offset(skip).limit(limit).all()

    return tasks


# -----------------------------
# Get Single Task
# -----------------------------

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: UUID, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# -----------------------------
# Update Task
# -----------------------------

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: UUID, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task_update.title is not None:
        task.title = task_update.title

    if task_update.description is not None:
        task.description = task_update.description

    db.commit()

    db.refresh(task)

    return task


# -----------------------------
# Toggle Completion
# -----------------------------

@app.patch("/tasks/{task_id}/complete", response_model=schemas.TaskResponse)
def toggle_task(task_id: UUID, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.completed = not task.completed

    db.commit()

    db.refresh(task)

    return task


# -----------------------------
# Delete Task
# -----------------------------

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()

    return None


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "Task Management API",
        "database": "PostgreSQL connected",
        "docs": "/docs"
    }
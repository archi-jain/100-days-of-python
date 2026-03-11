from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

import models
import schemas

from database import get_db


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):

    new_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority.value,
        due_date=task.due_date
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task


@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):

    return db.query(models.Task).all()


@router.get("/overdue", response_model=List[schemas.TaskResponse])
def overdue_tasks(db: Session = Depends(get_db)):

    now = datetime.utcnow()

    tasks = db.query(models.Task).filter(
        models.Task.completed == False,
        models.Task.due_date < now
    ).all()

    return tasks


@router.get("/upcoming", response_model=List[schemas.TaskResponse])
def upcoming_tasks(db: Session = Depends(get_db)):

    now = datetime.utcnow()

    future = now + timedelta(days=7)

    tasks = db.query(models.Task).filter(
        models.Task.completed == False,
        models.Task.due_date >= now,
        models.Task.due_date <= future
    ).all()

    return tasks
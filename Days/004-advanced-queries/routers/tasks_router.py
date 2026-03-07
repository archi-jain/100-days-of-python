from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import UUID

import models
import schemas

from database import get_db
from auth import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskResponse)

def create_task(

        task: schemas.TaskCreate,

        db: Session = Depends(get_db),

        current_user: models.User = Depends(get_current_user)

):

    new_task = models.Task(

        title=task.title,

        description=task.description,

        owner_id=current_user.id
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task


@router.get("/", response_model=List[schemas.TaskResponse])

def get_tasks(

    completed: Optional[bool] = Query(None),

    sort_by: str = Query("created_at"),

    order: str = Query("desc"),

    skip: int = Query(0, ge=0),

    limit: int = Query(20, ge=1, le=100),

    search: Optional[str] = Query(None),

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    query = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    )

    if completed is not None:

        query = query.filter(models.Task.completed == completed)


    if search:

        search_term = f"%{search}%"

        query = query.filter(
            or_(
                models.Task.title.ilike(search_term),
                models.Task.description.ilike(search_term)
            )
        )


    valid_sort_fields = ["created_at", "updated_at", "title", "completed"]

    if sort_by not in valid_sort_fields:
        sort_by = "created_at"

    column = getattr(models.Task, sort_by)

    if order == "desc":
        query = query.order_by(desc(column))
    else:
        query = query.order_by(asc(column))


    query = query.offset(skip).limit(limit)

    return query.all()


@router.get("/stats", response_model=schemas.TaskStatsResponse)

def get_task_stats(

        db: Session = Depends(get_db),

        current_user: models.User = Depends(get_current_user)

):

    user_tasks = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    )

    total = user_tasks.count()

    completed = user_tasks.filter(
        models.Task.completed == True
    ).count()

    pending = total - completed

    completion_rate = (completed / total * 100) if total else 0


    today_start = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    created_today = user_tasks.filter(
        models.Task.created_at >= today_start
    ).count()


    week_start = today_start - timedelta(days=today_start.weekday())

    created_this_week = user_tasks.filter(
        models.Task.created_at >= week_start
    ).count()


    return {

        "total": total,

        "completed": completed,

        "pending": pending,

        "completion_rate": round(completion_rate, 2),

        "created_today": created_today,

        "created_this_week": created_this_week

    }
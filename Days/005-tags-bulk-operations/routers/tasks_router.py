from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

import models
import schemas

from database import get_db
from auth import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


# -----------------------------
# CREATE TASK (Day 1 + Day 5 tags)
# -----------------------------
@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
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

    # Add tags if provided
    if task.tag_ids:

        tags = db.query(models.Tag).filter(
            models.Tag.id.in_(task.tag_ids),
            models.Tag.owner_id == current_user.id
        ).all()

        if len(tags) != len(task.tag_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more tags not found"
            )

        new_task.tags = tags

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# -----------------------------
# GET TASKS (Day 4 + Day 5 filtering)
# -----------------------------
@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(

    completed: Optional[bool] = Query(None),

    sort_by: str = Query("created_at"),

    order: str = Query("desc"),

    skip: int = Query(0, ge=0),

    limit: int = Query(20, ge=1, le=100),

    search: Optional[str] = Query(None),

    tag_id: Optional[UUID] = Query(None),

    tag_name: Optional[str] = Query(None),

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    query = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    )

    # Filter by completion
    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    # Filter by tag id
    if tag_id:
        query = query.filter(
            models.Task.tags.any(models.Tag.id == tag_id)
        )

    # Filter by tag name
    if tag_name:
        query = query.filter(
            models.Task.tags.any(models.Tag.name == tag_name.lower())
        )

    # Search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Task.title.ilike(search_term),
                models.Task.description.ilike(search_term)
            )
        )

    # Sorting
    valid_sort_fields = [
        "created_at",
        "updated_at",
        "title",
        "completed"
    ]

    if sort_by not in valid_sort_fields:
        sort_by = "created_at"

    column = getattr(models.Task, sort_by)

    if order == "desc":
        query = query.order_by(desc(column))
    else:
        query = query.order_by(asc(column))

    # Pagination
    query = query.offset(skip).limit(limit)

    return query.all()


# -----------------------------
# GET SINGLE TASK
# -----------------------------
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(

    task_id: UUID,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    return task


# -----------------------------
# UPDATE TASK
# -----------------------------
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(

    task_id: UUID,

    task_update: schemas.TaskUpdate,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    if task_update.title is not None:
        task.title = task_update.title

    if task_update.description is not None:
        task.description = task_update.description

    db.commit()
    db.refresh(task)

    return task


# -----------------------------
# TOGGLE COMPLETE
# -----------------------------
@router.patch("/{task_id}/complete", response_model=schemas.TaskResponse)
def toggle_complete(

    task_id: UUID,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    task.completed = not task.completed

    db.commit()
    db.refresh(task)

    return task


# -----------------------------
# DELETE TASK
# -----------------------------
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(

    task_id: UUID,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    db.delete(task)
    db.commit()

    return None


# -----------------------------
# ADD TAGS TO TASK (Day 5)
# -----------------------------
@router.post("/{task_id}/tags", response_model=schemas.TaskResponse)
def add_tags_to_task(

    task_id: UUID,

    tag_data: schemas.BulkUpdateTags,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    tags = db.query(models.Tag).filter(
        models.Tag.id.in_(tag_data.tag_ids),
        models.Tag.owner_id == current_user.id
    ).all()

    for tag in tags:
        if tag not in task.tags:
            task.tags.append(tag)

    db.commit()
    db.refresh(task)

    return task


# -----------------------------
# REMOVE TAG FROM TASK
# -----------------------------
@router.delete("/{task_id}/tags/{tag_id}", response_model=schemas.TaskResponse)
def remove_tag_from_task(

    task_id: UUID,

    tag_id: UUID,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    tag = db.query(models.Tag).filter(
        models.Tag.id == tag_id,
        models.Tag.owner_id == current_user.id
    ).first()

    if tag and tag in task.tags:
        task.tags.remove(tag)

    db.commit()
    db.refresh(task)

    return task


# -----------------------------
# BULK COMPLETE
# -----------------------------
@router.post("/bulk/complete", response_model=schemas.BulkOperationResponse)
def bulk_complete_tasks(

    bulk_data: schemas.BulkTaskIds,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    updated = db.query(models.Task).filter(
        models.Task.id.in_(bulk_data.task_ids),
        models.Task.owner_id == current_user.id
    ).update({"completed": True}, synchronize_session=False)

    db.commit()

    return {
        "updated": updated,
        "message": f"{updated} tasks marked complete"
    }


# -----------------------------
# BULK DELETE
# -----------------------------
@router.delete("/bulk", response_model=schemas.BulkOperationResponse)
def bulk_delete_tasks(

    bulk_data: schemas.BulkTaskIds,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user)

):

    deleted = db.query(models.Task).filter(
        models.Task.id.in_(bulk_data.task_ids),
        models.Task.owner_id == current_user.id
    ).delete(synchronize_session=False)

    db.commit()

    return {
        "deleted": deleted,
        "message": f"{deleted} tasks deleted"
    }


# -----------------------------
# TASK STATISTICS (Day 4)
# -----------------------------
@router.get("/stats")
def task_stats(

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

    completion_rate = (completed / total * 100) if total > 0 else 0

    today = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    created_today = user_tasks.filter(
        models.Task.created_at >= today
    ).count()

    week_start = today - timedelta(days=today.weekday())

    created_week = user_tasks.filter(
        models.Task.created_at >= week_start
    ).count()

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round(completion_rate, 2),
        "created_today": created_today,
        "created_this_week": created_week
    }
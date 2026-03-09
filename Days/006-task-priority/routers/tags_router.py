from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

import models
import schemas

from database import get_db
from auth import get_current_user


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=schemas.TagResponse)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    existing = db.query(models.Tag).filter(
        models.Tag.owner_id == current_user.id,
        models.Tag.name == tag.name
    ).first()

    if existing:
        raise HTTPException(400, "Tag already exists")

    new_tag = models.Tag(
        name=tag.name,
        color=tag.color,
        owner_id=current_user.id
    )

    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return new_tag


@router.get("/", response_model=List[schemas.TagResponse])
def get_tags(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    return db.query(models.Tag).filter(models.Tag.owner_id == current_user.id).all()


@router.delete("/{tag_id}")
def delete_tag(tag_id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    tag = db.query(models.Tag).filter(
        models.Tag.id == tag_id,
        models.Tag.owner_id == current_user.id
    ).first()

    if not tag:
        raise HTTPException(404, "Tag not found")

    db.delete(tag)
    db.commit()

    return {"message": "Tag deleted"}
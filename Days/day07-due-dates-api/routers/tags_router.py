from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas

from database import get_db


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=schemas.TagResponse)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):

    new_tag = models.Tag(name=tag.name, color=tag.color)

    db.add(new_tag)

    db.commit()

    db.refresh(new_tag)

    return new_tag


@router.get("/", response_model=List[schemas.TagResponse])
def get_tags(db: Session = Depends(get_db)):

    return db.query(models.Tag).all()
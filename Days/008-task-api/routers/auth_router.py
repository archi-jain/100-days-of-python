from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import get_db
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.UserResponse)

def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username exists")

    new_user = models.User(

        username=user.username,

        email=user.email,

        hashed_password=get_password_hash(user.password)
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=schemas.Token)

def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.username == user_credentials.username
    ).first()

    if not user or not verify_password(
        user_credentials.password,
        user.hashed_password
    ):

        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)

def get_me(current_user: models.User = Depends(get_current_user)):

    return current_user
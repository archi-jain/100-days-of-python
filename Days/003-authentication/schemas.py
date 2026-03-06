from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


# -----------------------
# User Schemas
# -----------------------

class UserCreate(BaseModel):

    username: str

    email: EmailStr

    password: str


class UserLogin(BaseModel):

    username: str

    password: str


class UserResponse(BaseModel):

    id: UUID

    username: str

    email: str

    is_active: bool

    created_at: datetime


    class Config:

        from_attributes = True


class Token(BaseModel):

    access_token: str

    token_type: str


# -----------------------
# Task Schemas
# -----------------------

class TaskCreate(BaseModel):

    title: str

    description: Optional[str]


class TaskUpdate(BaseModel):

    title: Optional[str]

    description: Optional[str]


class TaskResponse(BaseModel):

    id: UUID

    title: str

    description: Optional[str]

    completed: bool

    owner_id: UUID

    created_at: datetime

    updated_at: datetime


    class Config:

        from_attributes = True
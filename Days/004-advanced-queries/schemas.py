from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


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

    created_at: datetime

    updated_at: datetime

    owner_id: UUID

    class Config:
        from_attributes = True


class TaskStatsResponse(BaseModel):

    total: int

    completed: int

    pending: int

    completion_rate: float

    created_today: int

    created_this_week: int
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime
from enum import Enum


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TagCreate(BaseModel):
    name: str
    color: Optional[str] = None


class TagResponse(BaseModel):

    id: UUID
    name: str
    color: Optional[str]

    class Config:
        from_attributes = True


# class TaskCreate(BaseModel):

#     title: str

#     description: Optional[str] = None

#     priority: Optional[PriorityEnum] = PriorityEnum.medium

#     due_date: Optional[datetime] = None

#     tag_ids: Optional[List[UUID]] = []


class TaskUpdate(BaseModel):

    title: Optional[str] = None

    description: Optional[str] = None

    priority: Optional[PriorityEnum] = None

    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):

    id: UUID

    title: str

    description: Optional[str]

    completed: bool

    priority: str

    due_date: Optional[datetime]

    is_overdue: bool

    created_at: datetime

    updated_at: datetime

    owner_id: UUID

    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):

    title: str = Field(
        ...,
        max_length=100,
        description="Task title",
        examples=["Submit quarterly report"]
    )

    description: Optional[str] = Field(
        None,
        description="Task description",
        examples=["Prepare slides and submit"]
    )

    priority: Optional[PriorityEnum] = Field(
        default=PriorityEnum.medium,
        examples=["high"]
    )

    due_date: Optional[datetime] = Field(
        None,
        description="Task deadline",
        examples=["2026-03-15T17:00:00Z"]
    )

    tag_ids: Optional[List[UUID]] = []

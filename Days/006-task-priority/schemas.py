from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime
from enum import Enum


# ==========================================================
# PRIORITY ENUM (Day 6)
# ==========================================================

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# ==========================================================
# USER SCHEMAS (Authentication)
# ==========================================================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================================================
# TAG SCHEMAS
# ==========================================================

class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

    color: Optional[str] = Field(
        None,
        pattern="^#[0-9A-Fa-f]{6}$"
    )

    @field_validator("name")
    def clean_name(cls, v):
        v = v.strip().lower()

        if not v:
            raise ValueError("Tag name cannot be empty")

        return v


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)

    color: Optional[str] = Field(
        None,
        pattern="^#[0-9A-Fa-f]{6}$"
    )


class TagResponse(BaseModel):
    id: UUID
    name: str
    color: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================================
# TASK SCHEMAS
# ==========================================================

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100)

    description: Optional[str] = Field(None, max_length=500)

    priority: Optional[PriorityEnum] = Field(default=PriorityEnum.medium)

    tag_ids: Optional[List[UUID]] = []


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)

    description: Optional[str] = Field(None, max_length=500)

    priority: Optional[PriorityEnum] = None

    tag_ids: Optional[List[UUID]] = None


class TaskResponse(BaseModel):

    id: UUID

    title: str

    description: Optional[str]

    completed: bool

    priority: str

    created_at: datetime

    updated_at: datetime

    owner_id: UUID

    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


# ==========================================================
# BULK OPERATION SCHEMAS
# ==========================================================

class BulkTaskIds(BaseModel):

    task_ids: List[UUID] = Field(..., min_length=1, max_length=100)


class BulkUpdateTags(BaseModel):

    tag_ids: List[UUID] = Field(..., min_length=1, max_length=20)


class BulkOperationResponse(BaseModel):

    updated: Optional[int] = None

    deleted: Optional[int] = None

    message: str


# ==========================================================
# TASK STATS RESPONSE
# ==========================================================

class TaskStatsResponse(BaseModel):

    total: int

    completed: int

    pending: int

    completion_rate: float

    created_today: int

    created_this_week: int

    by_priority: Dict[str, int]
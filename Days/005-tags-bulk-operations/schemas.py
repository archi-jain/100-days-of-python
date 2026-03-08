from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# ==============================
# USER SCHEMAS (Day 3)
# ==============================

class UserCreate(BaseModel):

    username: str = Field(..., min_length=3, max_length=50)

    email: EmailStr

    password: str = Field(..., min_length=6)


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


class TokenData(BaseModel):

    username: Optional[str] = None


# ==============================
# TAG SCHEMAS (Day 5)
# ==============================

class TagCreate(BaseModel):

    name: str = Field(..., min_length=1, max_length=50)

    color: Optional[str] = Field(
        None,
        pattern="^#[0-9A-Fa-f]{6}$"
    )


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


# ==============================
# TASK SCHEMAS
# ==============================

class TaskCreate(BaseModel):

    title: str = Field(..., max_length=100)

    description: Optional[str] = Field(None, max_length=500)

    tag_ids: Optional[List[UUID]] = []


class TaskUpdate(BaseModel):

    title: Optional[str] = Field(None, max_length=100)

    description: Optional[str] = Field(None, max_length=500)

    tag_ids: Optional[List[UUID]] = None


class TaskResponse(BaseModel):

    id: UUID

    title: str

    description: Optional[str]

    completed: bool

    created_at: datetime

    updated_at: datetime

    owner_id: UUID

    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


# ==============================
# BULK OPERATIONS (Day 5)
# ==============================

class BulkTaskIds(BaseModel):

    task_ids: List[UUID] = Field(
        ...,
        min_items=1,
        max_items=100
    )


class BulkUpdateTags(BaseModel):

    task_ids: List[UUID]

    tag_ids: List[UUID]


class BulkOperationResponse(BaseModel):

    updated: Optional[int] = None

    deleted: Optional[int] = None

    message: str


# ==============================
# TASK STATS (Day 4)
# ==============================

class TaskStatsResponse(BaseModel):

    total: int

    completed: int

    pending: int

    completion_rate: float

    created_today: int

    created_this_week: int
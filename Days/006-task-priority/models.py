from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database import Base


# Many-to-many association table
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String(50), unique=True, nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    tags = relationship("Tag", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(100), nullable=False, index=True)

    description = Column(String(500))

    completed = Column(Boolean, default=False)

    priority = Column(String(10), default="medium", index=True)   # NEW DAY-6

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="tasks")

    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")


class Tag(Base):

    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(50), nullable=False)

    color = Column(String(7))

    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="tags")

    tasks = relationship("Task", secondary=task_tags, back_populates="tags")

    __table_args__ = (
        Index("idx_owner_tag", "owner_id", "name", unique=True),
    )
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime
import uuid

from database import Base


task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id")),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id")),
)


class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String, unique=True)

    email = Column(String, unique=True)

    hashed_password = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner")

    tags = relationship("Tag", back_populates="owner")


class Tag(Base):

    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String)

    color = Column(String)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    owner = relationship("User", back_populates="tags")

    tasks = relationship("Task", secondary=task_tags, back_populates="tags")


class Task(Base):

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String)

    description = Column(String)

    completed = Column(Boolean, default=False)

    priority = Column(String, default="medium")

    due_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")

    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")


    @hybrid_property
    def is_overdue(self):

        if self.completed:
            return False

        if self.due_date is None:
            return False

        return self.due_date < datetime.utcnow()
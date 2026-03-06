from fastapi import FastAPI

import models
from database import engine

from routers import auth_router, tasks_router


# Create database tables automatically
# In production we use migrations instead
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Management API with Authentication",
    description="FastAPI project with PostgreSQL, JWT authentication, and secure task management",
    version="3.0.0"
)


# Register routers
app.include_router(auth_router.router)
app.include_router(tasks_router.router)


@app.get("/")
def root():
    return {
        "message": "Task Management API",
        "version": "3.0.0",
        "features": [
            "JWT Authentication",
            "User Registration",
            "Secure Task Management",
            "PostgreSQL Database"
        ]
    }
from fastapi import FastAPI

import models
from database import engine

from routers import auth_router, tasks_router


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Management API",
    version="4.0.0",
    description="FastAPI backend with authentication and advanced query features"
)


app.include_router(auth_router.router)
app.include_router(tasks_router.router)


@app.get("/")
def root():
    return {
        "message": "Task Management API",
        "features": [
            "JWT Authentication",
            "Advanced Filtering",
            "Sorting",
            "Pagination",
            "Search",
            "Statistics"
        ]
    }
from fastapi import FastAPI

import models
from database import engine

from routers import auth_router
from routers import tasks_router
from routers import tags_router


# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    version="6.0.0",
    description="Task API with authentication, tags, bulk ops and priority",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# include routers
app.include_router(auth_router.router)
app.include_router(tasks_router.router)
app.include_router(tags_router.router)


@app.get("/")
def root():
    return {
        "message": "Task Management API",
        "version": "6.0.0"
    }
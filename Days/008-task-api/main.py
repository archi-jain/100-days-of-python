from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

import models
from database import engine, SessionLocal
from routers import auth_router, tasks_router, tags_router


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Management API",
    description="""
Complete task management system with:

• JWT Authentication  
• Tasks with priority and due dates  
• Tag system  
• Advanced filtering  
• Bulk operations  
• Analytics endpoints  
""",
    version="1.0.0",
    contact={
        "name": "Archi Jain",
        "url": "https://github.com/archi-jain",
    },
    openapi_tags=[
        {"name": "Authentication", "description": "User login and registration"},
        {"name": "Tasks", "description": "Task CRUD operations"},
        {"name": "Tags", "description": "Tag management"},
        {"name": "System", "description": "Health and API info"},
    ],
)


# -------------------------------
# CORS (for frontend)
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Validation Error Handler
# -------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    errors = []

    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors,
                "timestamp": datetime.utcnow().isoformat()
            }
        },
    )


# -------------------------------
# Routers
# -------------------------------

app.include_router(auth_router.router, tags=["Authentication"])
app.include_router(tasks_router.router, tags=["Tasks"])
app.include_router(tags_router.router, tags=["Tags"])


# -------------------------------
# API Root
# -------------------------------

@app.get("/", tags=["System"], summary="API Info")
def root():

    return {
        "name": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# -------------------------------
# Health Check
# -------------------------------

@app.get("/health", tags=["System"], summary="Health Check")
def health_check():

    db_status = "healthy"

    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status
    }
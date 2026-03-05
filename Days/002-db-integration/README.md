# Day 002 – FastAPI + PostgreSQL

Today I upgraded my Task Management API to use PostgreSQL instead of in-memory storage.

## What I Learned

- PostgreSQL database setup
- SQLAlchemy ORM
- Database session management
- Dependency injection in FastAPI
- Persistent data storage

## Key Concepts

SQLAlchemy ORM
Database Sessions
Connection pooling
UUID primary keys
Environment variables

## Run the API

pip install -r requirements.txt

uvicorn main:app --reload

Open docs:

http://127.0.0.1:8000/docs
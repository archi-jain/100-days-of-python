# Day 1 Challenge - Task Management API

Build a REST API using FastAPI with the following features:

## Required Features

- Create a task
- Get all tasks
- Get task by ID
- Update a task
- Delete a task
- Mark task complete/incomplete

## Task Model

id (UUID)
title (string, required, max 100)
description (string, optional, max 500)
completed (boolean)
created_at (timestamp)
updated_at (timestamp)

## Technical Requirements

- FastAPI framework
- Pydantic models
- In-memory storage
- Proper HTTP status codes
- API documentation

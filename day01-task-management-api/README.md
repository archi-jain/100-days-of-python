# Day 1 - Task Management API (FastAPI)

## Overview

This project implements a RESTful Task Management API using FastAPI.

The API allows users to create, update, delete, and manage tasks.

## Features

- Create tasks
- Retrieve all tasks
- Retrieve a single task
- Update tasks
- Toggle completion status
- Delete tasks
- Filtering and pagination
- Health check endpoint

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn

## Run the API

Install dependencies

pip install -r requirements.txt

Start server

uvicorn main:app --reload

Open API documentation

http://127.0.0.1:8000/docs

## Key Learnings

- FastAPI routing
- Pydantic validation
- REST API design
- UUID generation
- Async endpoints
- In-memory data storage

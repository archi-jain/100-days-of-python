# Day 1 - Task Management API (FastAPI)

## Overview

This project implements a RESTful Task Management API using FastAPI.

The API allows users to create, update, delete, and manage tasks.

## Features

- Create task
- Get all tasks
- Get task by ID
- Update task
- Toggle completion
- Delete task

## Tech Stack

Python
FastAPI
Pydantic

## Run Locally

pip install -r requirements.txt

uvicorn main:app --reload

## API Documentation

http://localhost:8000/docs

## Example Request

POST /tasks

{
"title": "Learn FastAPI",
"description": "Build a REST API"
}
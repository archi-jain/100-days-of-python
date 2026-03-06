003-authentication/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
│
├── routers/
│   ├── auth_router.py
│   └── tasks_router.py
│
├── requirements.txt
├── .env
├── challenge.md
└── README.md




# Day 3 – Authentication with JWT

This project extends the FastAPI Task API with user authentication.

## Features

- User registration
- Login with JWT tokens
- Secure password hashing
- Protected API routes
- Task ownership per user

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Passlib bcrypt

## Run the Project

Install dependencies

pip install -r requirements.txt

Run server

uvicorn main:app --reload

Open API Docs

http://localhost:8000/docs

## Learning Outcomes

- JWT authentication
- Password hashing
- OAuth2 token authentication
- Dependency injection
- Secure API design



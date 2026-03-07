004-advanced-queries/
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


# Day 4 – Advanced Query API

FastAPI backend with authentication and advanced query features.

## Features

JWT Authentication  
User-owned tasks  
Filtering  
Sorting  
Pagination  
Search  
Statistics  

## Run

Install dependencies

pip install -r requirements.txt

Run server

uvicorn main:app --reload

Open API Docs

http://localhost:8000/docs
# Day 3 Challenge – JWT Authentication

Upgrade the Task API with authentication.

Features implemented:

- User registration
- Login endpoint
- JWT token authentication
- Password hashing using bcrypt
- Protected routes
- Task ownership per user

Endpoints added:

POST /auth/register  
POST /auth/login  
GET /auth/me  

All task endpoints require authentication.

Security concepts learned:

- Password hashing
- JWT tokens
- OAuth2 scheme
- Protected routes
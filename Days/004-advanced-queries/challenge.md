# Day 4 – Advanced Query Features

Added advanced query features to Task API.

Features:

Filtering  
Sorting  
Pagination  
Search  
Statistics endpoint  
Database indexing  

Example queries:

GET /tasks?completed=true  
GET /tasks?search=meeting  
GET /tasks?sort_by=title&order=asc  
GET /tasks?skip=20&limit=10  
GET /tasks/stats
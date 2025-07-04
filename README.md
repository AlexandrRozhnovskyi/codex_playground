# Habit Tracker Example

This repository contains a minimal full‑stack habit tracker with a FastAPI backend and a React frontend.

## Requirements

- Docker
- docker-compose

## Running the project

```bash
docker-compose up --build
```

The frontend will be available at [http://localhost:3000](http://localhost:3000) and the backend Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs).

### Backend Swagger
Open your browser at `http://localhost:8000/docs` to explore the API.

### Frontend
Open [http://localhost:3000](http://localhost:3000) after running `docker-compose up`.

### Manual API check
Example using `curl` to create a user:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}' \
  http://localhost:8000/users
```

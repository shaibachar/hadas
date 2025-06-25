# PDF to Audio Converter

This is a full-stack project with a FastAPI backend and a ReactJS frontend. Both are Dockerized and orchestrated with Docker Compose. Backend and frontend each have .env files for dev and prod.

## Project Structure
- `backend/`: FastAPI backend (Python, pipenv)
- `frontend/`: ReactJS frontend
- `docker-compose.yml`: Orchestrates both services

## Quick Start

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
2. Backend: http://localhost:8000
3. Frontend: http://localhost:3000

## Development
- Edit backend and frontend code in their respective folders.
- Use `.env.dev` and `.env.prod` for environment variables.

## Production
- Adjust `.env.prod` files and Docker Compose as needed.

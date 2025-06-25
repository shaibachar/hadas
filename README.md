# PDF to Audio Converter

This is a full-stack project with a FastAPI backend and a ReactJS frontend. Both are Dockerized and orchestrated with Docker Compose. Backend and frontend each have .env files for dev and prod.

## Features

- **Convert Webpage Link to Audio**: Enter a URL and get an audio file reading the page's text.
- **Convert PDF to Text and Audio**: Upload a PDF and receive both the extracted text (as a downloadable file) and an audio file reading the text.
- **Convert Text to Audio**: Paste or type any text and generate an audio file.
- **Mobile Friendly UI**: Responsive React frontend for desktop and mobile.
- **Integration Tests**: Automated tests for all API endpoints (link-to-audio, text-to-audio, PDF upload) run on `docker-compose up`.
- **Unit Tests**: Core backend functions are covered by unit tests.

## Screenshots

### Home Page
<!-- Place a screenshot of the home page here -->

### Link to Audio
<!-- Place a screenshot of the link-to-audio feature here -->

### PDF to Text & Audio
<!-- Place a screenshot of the PDF upload and results here -->

### Text to Audio
<!-- Place a screenshot of the text-to-audio feature here -->

## Project Structure
- `backend/`: FastAPI backend (Python, pipenv)
- `frontend/`: ReactJS frontend
- `docker-compose.yml`: Orchestrates both services

## Quick Start

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
2. Backend: http://localhost:8080
3. Frontend: http://localhost:3000

## Development
- Edit backend and frontend code in their respective folders.
- Use `.env.dev` and `.env.prod` for environment variables.

## Production
- Adjust `.env.prod` files and Docker Compose as needed.

## Testing
- **Integration tests** run automatically on `docker-compose up` and cover all main features.
- **Unit tests** can be run inside the backend container:
  ```bash
  pipenv run pytest test_unit.py
  ```

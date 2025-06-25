#!/bin/bash
# Run both backend (FastAPI) and frontend (React) servers without Docker

# Find a suitable python version (prefer 3.11, fallback to python3)
PYTHON_BIN=$(command -v python3.11 || command -v python3)
if [ -z "$PYTHON_BIN" ]; then
  echo "Python 3.11 or python3 not found. Please install Python."
  exit 1
fi

# Start backend
cd "$(dirname "$0")/backend"
echo "[Backend] Installing Python dependencies with pipenv..."
pipenv --python "$PYTHON_BIN" install --dev

echo "[Backend] Starting FastAPI server on http://localhost:8000 ..."
pipenv run uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
if [ ! -d "node_modules" ]; then
  echo "[Frontend] Installing npm dependencies..."
  npm install
fi

echo "[Frontend] Starting React development server on http://localhost:3000 ..."
npm start &
FRONTEND_PID=$!

# Wait for both processes
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait $BACKEND_PID $FRONTEND_PID

# Use an official Python runtime as a parent image
FROM python:3.11-slim

WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Install requests and fpdf for integration testing
RUN pip install requests fpdf

# Install coreutils (for sleep) in the backend Docker image
RUN apt-get update && apt-get install -y coreutils && rm -rf /var/lib/apt/lists/*

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 8080

# Command to run the app
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

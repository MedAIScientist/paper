FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml .
COPY README.md .

# Install dependencies with specific versions
RUN pip install --no-cache-dir \
    fastapi==0.68.0 \
    uvicorn==0.15.0 \
    python-multipart==0.0.6 \
    pydantic==1.8.0

# Install paper-qa
RUN pip install --no-cache-dir "paper-qa[local]"

# Copy the application code
COPY . .

# Create a directory for papers
RUN mkdir -p /app/papers

# Expose the port for the API
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "paperqa.api:app", "--host", "0.0.0.0", "--port", "8000"] 
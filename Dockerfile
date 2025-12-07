# Use official Python slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code
COPY src/ ./src/

# Expose port 8000
EXPOSE 8000

# Start FastAPI (entry point is src/main.py)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

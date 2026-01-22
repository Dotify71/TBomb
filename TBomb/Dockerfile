FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
COPY requirements-async.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-async.txt

# Copy application code
COPY . .

# Create database directory
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV DATABASE_PATH=/app/data/tbomb.db

# Expose port for potential web interface
EXPOSE 8000

# Create non-root user
RUN useradd -m -u 1000 tbomb && chown -R tbomb:tbomb /app
USER tbomb

# Default command
CMD ["python", "bomber_async.py"]
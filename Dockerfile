FROM python:3.11-slim

# Set non-interactive frontend to prevent debconf errors
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install sqlite3 for database operations
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Create directory for data
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV SECRET_KEY=change-this-in-production

# Start the Flask application directly.
# NOTE: scripts/init_website.sh is a HOST-level orchestration helper
# (it checks for Docker and runs `docker compose up`). It must NOT run
# inside the container — doing so caused the container to exit 1 on the
# "Docker is not installed" prerequisite check and crash-loop, which in
# turn made nginx's "app:5000" upstream unresolvable.
CMD ["python3", "app.py"]
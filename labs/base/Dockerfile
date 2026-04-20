FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for layer caching.
COPY base/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy framework and lab code.
COPY . .

# Make entrypoint executable.
RUN chmod +x base/entrypoint.sh

ENTRYPOINT ["base/entrypoint.sh"]

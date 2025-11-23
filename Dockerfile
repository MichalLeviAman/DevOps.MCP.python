# Dockerfile for DevOpsMCP - Google Cloud Run
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements-cloudrun.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ app/
COPY schema_sqlite.sql .
COPY mcp.json .

# Create database on startup
RUN python -c \"import sqlite3; from pathlib import Path; db = Path('devopsmcp.db'); schema = Path('schema_sqlite.sql'); conn = sqlite3.connect(db); conn.executescript(open(schema, encoding='utf-8').read()); conn.close(); print('Database initialized')\"

# Expose port (Cloud Run will set PORT env var)
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD exec uvicorn app.main_with_db:app --host 0.0.0.0 --port ${PORT}

# Python Image
FROM python:3.11-slim

# Avoid interactive prompts during package installation
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install SQLite3 for the seed script
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the dependency files and paste in .
COPY pyproject.toml .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir .

# Copy all and paste the rest of the application code
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Command to run the application and seed data
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 --reload & sleep 10 &&  python seed_py.py && wait"
# CMD sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 --reload & sleep 10 &&  seed_data.sh && wait"

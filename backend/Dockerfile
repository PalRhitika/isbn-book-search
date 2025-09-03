# Use official slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (optional, add if using psycopg2)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port 10000 internally (doesn’t have to match Render’s $PORT)
EXPOSE 10000

# Run migrations first, then start Gunicorn on Render's dynamic port
CMD ["sh", "-c", "python manage.py migrate && gunicorn isbn_book_search_system.wsgi:application -b 0.0.0.0:$PORT -w 3"]

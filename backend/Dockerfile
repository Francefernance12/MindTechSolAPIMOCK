# Use a slim Python image for a smaller footprint
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY . .

# Initialize the database and seed it (only for showcase purposes)
# In a real production app, this would be handled differently.
RUN python models.py && python seed.py

# Expose the Flask port
EXPOSE 5000

# Run the application with Gunicorn
# Binding to 0.0.0.0 allows access from outside the container
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

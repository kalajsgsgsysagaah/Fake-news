# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r Requirements.txt

# Copy project files
COPY . .

# Expose port (Railway uses dynamic PORT)
EXPOSE 7860

# Start app
CMD ["python", "app.py"]

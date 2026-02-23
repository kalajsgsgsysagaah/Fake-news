# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements first
COPY Requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r Requirements.txt

# Copy all files
COPY . .

# Railway dynamic port
ENV PORT=8080
EXPOSE 8080

# Start app
CMD ["python", "fake.py"]

# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir gradio requests

# Expose Gradio port
EXPOSE 7860

# Environment variables
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Run the app
CMD ["python", "app.py"]

# Use the official Python 3.9 image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libcairo2-dev \
    libgirepository1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade sqlalchemy
RUN pip install --upgrade faiss-cpu

# Expose the port for Gradio
EXPOSE 7860

# Copy your application files into the container
COPY . .

# Define the command to run your application
CMD ["python", "app.py"]
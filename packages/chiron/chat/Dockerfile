# Use a lightweight Python base image
FROM python:3.11-slim

# Set a working directory for the container
WORKDIR /app

# Copy local code to the container image
COPY . /app

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the app when the container starts
CMD ["python", "main.py"]

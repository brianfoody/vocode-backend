# Use the official Python base image
FROM python:3.9

# Install system packages
RUN apt-get update && \
    apt-get install -y portaudio19-dev ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY main.py .

# Expose the port the app will run on
EXPOSE 3001

# Start the application
CMD ["python", "main.py"]
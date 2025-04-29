# Start with the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install flask pymongo requests

# Expose port for the workout service
EXPOSE 5003

# Command to run the Flask app
CMD ["python", "app.py"]

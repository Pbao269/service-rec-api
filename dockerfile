# Use an official lightweight Python image as the base
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose port 8000 for the API
EXPOSE 8000

# Define the command to run your application using uvicorn
CMD ["uvicorn", "service_rec:app", "--host", "0.0.0.0", "--port", "8000"]

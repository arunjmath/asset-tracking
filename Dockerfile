# Use an official Python image
FROM python:3.10-slim



# Set working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask pymongo

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

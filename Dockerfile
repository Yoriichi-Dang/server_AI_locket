# Use Python 3.9 as base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Upgrade pip to avoid outdated errors
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
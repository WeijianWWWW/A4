# Use official Python image
FROM python:3.10-slim

# Install system dependencies for GeoPandas
RUN apt-get update && apt-get install -y \
    g++ \
    gcc \
    libproj-dev \
    proj-data \
    proj-bin \
    libgeos-dev \
    libgdal-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . /app

# Expose port
EXPOSE 8000

# Start the Dash app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:server"]

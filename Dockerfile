# Base image
FROM python:3.12-slim

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including GDAL
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    binutils \
    libproj-dev \
    libgeos-dev \
    libpq-dev \
    gcc \
    g++ \
    curl \
    wget \
    nano \
    git \
    && ln -s /usr/lib/libgdal.so.* /usr/lib/libgdal.so \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables required by GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# Set working directory
WORKDIR /ride_server

# Copy requirements and install Python packages
COPY requirements.txt .

# Use virtualenv if desired
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Add venv to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy Django project
COPY . .

# Expose port
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

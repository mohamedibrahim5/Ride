FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies including GDAL and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Find and set GDAL library path (more reliable than hardcoding)
RUN gdalinfo --version && \
    export GDAL_VERSION=$(gdal-config --version) && \
    echo "GDAL version: $GDAL_VERSION" && \
    export GDAL_LIBRARY_PATH=$(gdal-config --libs | awk '{print $1}' | sed 's/-L//' | sed 's/-lgdal//')/libgdal.so && \
    echo "GDAL library path: $GDAL_LIBRARY_PATH"

# Set environment variables (including fallback if detection fails)
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so \
    LD_LIBRARY_PATH=/usr/lib

WORKDIR /ride_server

COPY requirements.txt /ride_server/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /ride_server/

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
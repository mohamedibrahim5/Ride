FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 1. Install system dependencies for GDAL and other required tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Set GDAL environment variables (detect automatically)
RUN gdalinfo --version && \
    export GDAL_VERSION=$(gdal-config --version) && \
    echo "GDAL version: $GDAL_VERSION" && \
    pip install GDAL==$(gdal-config --version | cut -d. -f1-2)

# 3. Set library paths
ENV GDAL_LIBRARY_PATH="/usr/lib/libgdal.so" \
    GEOS_LIBRARY_PATH="/usr/lib/libgeos_c.so" \
    LD_LIBRARY_PATH="/usr/lib"

WORKDIR /ride_server

# 4. Install Python dependencies in two steps for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
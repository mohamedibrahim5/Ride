FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies with explicit versions
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    binutils \
    libproj-dev \
    libgdal-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV GDAL_LIBRARY_PATH="/usr/lib/libgdal.so" \
    GEOS_LIBRARY_PATH="/usr/lib/libgeos_c.so" \
    LD_LIBRARY_PATH="/usr/lib"

WORKDIR /ride_server

# Install Python dependencies in two stages for better caching
COPY requirements.txt .

# First install GDAL with system package (avoids compilation)
RUN apt-get update && \
    apt-get install -y python3-gdal && \
    pip install --upgrade pip && \
    pip install --no-cache-dir GDAL==$(gdal-config --version | cut -d. -f1-2) --no-binary GDAL

# Then install other requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
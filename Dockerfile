FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 1. First install dependencies without version pinning
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

# 2. Find and verify the installed GDAL version
RUN gdalinfo --version

# 3. Set environment variables
ENV GDAL_LIBRARY_PATH="/usr/lib/libgdal.so" \
    GEOS_LIBRARY_PATH="/usr/lib/libgeos_c.so" \
    LD_LIBRARY_PATH="/usr/lib"

WORKDIR /ride_server

# 4. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Install matching Python GDAL package
RUN pip install GDAL==$(gdal-config --version | cut -d. -f1-2)

COPY . .

EXPOSE 8000
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
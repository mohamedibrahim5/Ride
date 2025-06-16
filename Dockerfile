FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 1. Install system dependencies (GDAL 3.4.1)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    binutils \
    libproj-dev \
    libgdal-dev=3.4.1+dfsg-1 \
    gdal-bin=3.4.1+dfsg-1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Set GDAL paths (Debian Buster default locations)
ENV GDAL_LIBRARY_PATH="/usr/lib/libgdal.so" \
    GEOS_LIBRARY_PATH="/usr/lib/libgeos_c.so" \
    LD_LIBRARY_PATH="/usr/lib"

WORKDIR /ride_server

# 3. Install Python dependencies first (for caching)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Install GDAL Python package (MUST match system version)
RUN pip install GDAL==3.4.1  # Must match `libgdal-dev` version

COPY . .

EXPOSE 8000
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
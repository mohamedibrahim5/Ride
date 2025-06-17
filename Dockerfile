# Use GDAL Ubuntu-based image
FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

# Environment config
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system & Python dependencies including GDAL
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    gcc \
    g++ \
    net-tools \
    curl \
    wget \
    nano \
 && rm -rf /var/lib/apt/lists/*

# Set GDAL paths for Django
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# (Optional) Log the GDAL version to a file — for debugging
RUN gdal-config --version > /gdal_version.txt

# Set up Python virtual environment
ENV VENV_PATH="/opt/venv"
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

# Set workdir
WORKDIR /ride_server

# Copy project files
COPY . /ride_server/

# Install Python requirements inside virtualenv
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

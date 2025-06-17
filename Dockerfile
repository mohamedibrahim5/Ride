FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system and GDAL dependencies
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

# Set GDAL env vars
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV GDAL_VERSION=$(gdal-config --version)

# Set up virtualenv
ENV VENV_PATH="/opt/venv"
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

WORKDIR /ride_server
COPY . /ride_server/

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

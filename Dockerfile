FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies + Python venv
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    libpq-dev \
    gcc \
    g++ \
    net-tools \
    curl \
    wget \
    nano \
 && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
ENV VENV_PATH="/opt/venv"
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

WORKDIR /ride_server
COPY . /ride_server/

# Now pip install safely within virtualenv
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    python3-pip \
    libpq-dev \
    gcc \
    g++ \
    net-tools \
    curl \
    wget \
    nano \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /ride_server

COPY . /ride_server/

RUN python3 -m pip install --upgrade pip --break-system-packages \
 && python3 -m pip install --break-system-packages -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

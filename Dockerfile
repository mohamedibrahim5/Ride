FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    net-tools \
    curl \
    wget \
    nano \
    gdal-bin \
    libgdal-dev \
 && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set this to match `gdal-config --version`
ENV GDAL_VERSION=3.0.4

WORKDIR /ride_server


COPY . /ride_server/

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

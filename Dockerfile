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
    python3-gdal \
 && rm -rf /var/lib/apt/lists/*

# Optional: help GDAL find headers
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN mkdir -p /ride_server/logs && chown -R root:root /ride_server/logs

WORKDIR /ride_server

COPY . /ride_server/

# ✅ Avoid installing GDAL from PyPI again
RUN sed -i '/^gdal==/d' requirements.txt || true
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.10-slim-buster

# Recommended for containers:
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# 1️⃣ Install build tools + GDAL runtime + GDAL headers + Postgres driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev gcc g++ net-tools curl wget nano \
    gdal-bin libgdal-dev

# 2️⃣ Optional: verify GDAL version
RUN gdalinfo --version

# 3️⃣ Add logs folder
RUN mkdir -p /ride_server/logs && chown -R root:root /ride_server/logs

WORKDIR /ride_server

COPY . /ride_server/

# 4️⃣ Tell pip to match your system GDAL version
#    Check your gdalinfo output and match it.
#    For example, if you see 3.4.x:
#      pip install GDAL==3.4.1
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 5️⃣ (OPTIONAL) For safety: set GDAL_LIBRARY_PATH to the known installed lib
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

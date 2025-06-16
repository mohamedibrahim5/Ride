FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# ✅ Install GDAL runtime + headers + build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev gcc g++ net-tools curl wget nano \
    gdal-bin libgdal-dev

# ✅ Confirm GDAL version
RUN gdalinfo --version

# ✅ Create logs folder
RUN mkdir -p /ride_server/logs && chown -R root:root /ride_server/logs

WORKDIR /ride_server

COPY . /ride_server/

# ✅ Upgrade pip & install exact GDAL version
# Check version: `gdal-config --version`
RUN pip install --upgrade pip && \
    pip install GDAL==3.4.1 && \
    pip install -r requirements.txt

# ✅ Explicit GDAL lib path for Django
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies incl. GDAL
RUN apt-get update && \
    apt-get -y install libpq-dev gcc net-tools curl wget nano \
    gdal-bin libgdal-dev

# Explicitly ensure the library path is set
ENV GDAL_LIBRARY_PATH=/lib/libgdal.so
ENV LD_LIBRARY_PATH=/lib

WORKDIR /ride_server

COPY . /ride_server/

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

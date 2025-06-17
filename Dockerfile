FROM osgeo/gdal:alpine-small-latest

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apk update && apk add \
    python3 py3-pip py3-wheel py3-setuptools \
    build-base libffi-dev \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /ride_server

COPY . /ride_server/

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

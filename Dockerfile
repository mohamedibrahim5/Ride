FROM osgeo/gdal:3.6.2-python3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install extra dependencies
RUN apt-get update && apt-get install -y \
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

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.10-slim-buster

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc net-tools curl wget nano

# create a logs folder so redirection or Django file handlers can write to it
RUN mkdir -p /ride_server/logs && chown -R root:root /ride_server/logs


# Set work directory
WORKDIR /ride_server

# Copy project
COPY . /ride_server/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

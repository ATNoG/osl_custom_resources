FROM python:3.11-slim

# Install required system packages for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

COPY ./src /opt/app
RUN pip3 install -r requirements.txt


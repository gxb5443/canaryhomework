FROM python:3

MAINTAINER Gian Biondi

WORKDIR /usr/src/app

ENV FLASK_APP /usr/src/app/app.py

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./migrations/ ./migrations
COPY ./app.py .
COPY ./config.py .
COPY ./models.py .
COPY ./invalid_usage.py .

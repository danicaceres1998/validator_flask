FROM python:3.6.13-buster

# Libs and Config
RUN apt-get update -qq && apt-get install -y sqlite3 vim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
ENV SENTRY_KEY='https://examplePublicKey@o0.ingest.sentry.io/0'
# API Code
COPY . .
RUN python3 apiconfiguration.py

CMD uwsgi --ini proyect-uwsgi.ini
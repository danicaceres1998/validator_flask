FROM python:3.6.13-buster

# Libs and Config
RUN apt-get update -qq && apt-get install -y sqlite3 vim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
# API Code
COPY . .
RUN python3 dbconfiguration.py

CMD uwsgi --ini proyect-uwsgi.ini
FROM python:3.4.2

WORKDIR /validator_app

RUN mkdir app/

COPY app/ /validator_app/app
COPY proyect-uwsgi.ini /validator_app

RUN python3 -m venv env
RUN pip install flask 
RUN pip install flask-restful
RUN pip install uwsgi

CMD uwsgi --ini proyect-uwsgi.ini
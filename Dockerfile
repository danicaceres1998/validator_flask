FROM python:3.8.0

RUN pip3 install --upgrade pip

WORKDIR /validator_app

COPY . /validator_app

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "app/__init__.py"]
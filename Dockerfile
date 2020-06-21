FROM python:3.8.0

RUN pip3 install --upgrade pip

WORKDIR /validator_app

COPY . /validator_app

RUN pip3 --no-cache-dir install -r requirements.txt

CMD uwsgi --http 127.0.0.1:3031 \
    --wsgi-file app/__init__.py \
    --callable app \
    --processes 4 \
    --threads 2 \
    --stats 127.0.0.1:919
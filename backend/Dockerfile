FROM python:3.8-alpine

RUN apk add build-base linux-headers  # To build uWSGI

COPY . /app
WORKDIR /app

RUN python -m pip install -r requirements.txt

CMD [ "uwsgi", "--socket", "0.0.0.0:5000", \
               "--protocol", "http", \
               "--wsgi", "app:app" ]

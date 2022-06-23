FROM python:3.10.3-slim

WORKDIR /telebot
ADD . . 

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r requirements.txt


CMD ["python", "main.py"]
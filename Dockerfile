FROM python:3.9

RUN mkdir usr/src/account-back/ &&\
    mkdir usr/src/account-back/django_app

WORKDIR /usr/src/account-back/

COPY ./ .

RUN pip install -r requirements.txt

WORKDIR ./django_app